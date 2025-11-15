from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from services.llm.llm_service import LLMService
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class MatchingStrategy(ABC):
    @abstractmethod
    async def calculate_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

class LLMMatchingStrategy(MatchingStrategy):
    def __init__(self):
        self.llm_service = LLMService()
        self.weight_config = {
            'skills': 0.35,
            'experience': 0.30,
            'education': 0.20,
            'location': 0.10,
            'keywords': 0.05
        }
    
    async def calculate_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resume_text = self._prepare_resume_text(resume_data)
            job_description = self._prepare_job_description(job_data)
            
            llm_analysis = await self.llm_service.analyze_match(resume_text, job_description)
            
            enhanced_analysis = self._enhance_analysis(llm_analysis, resume_data, job_data)
            
            match_result = {
                'overall_score': enhanced_analysis.get('overall_score', 0),
                'matched_skills': enhanced_analysis.get('matched_skills', []),
                'skill_gaps': enhanced_analysis.get('skill_gaps', []),
                'transferable_skills': enhanced_analysis.get('transferable_skills', []),
                'experience_match': enhanced_analysis.get('experience_match', 0),
                'education_match': enhanced_analysis.get('education_match', 0),
                'location_match': enhanced_analysis.get('location_match', 0),
                'recommendations': enhanced_analysis.get('recommendations', []),
                'calculated_at': datetime.utcnow().isoformat(),
                'scoring_breakdown': self._calculate_breakdown(enhanced_analysis)
            }
            
            return match_result
            
        except Exception as e:
            logger.error(f"Error in LLM matching strategy: {e}")
            return self._create_fallback_result(resume_data, job_data)
    
    def _prepare_resume_text(self, resume_data: Dict[str, Any]) -> str:
        sections = []
        
        if 'personal_info' in resume_data:
            info = resume_data['personal_info']
            sections.append(f"Name: {info.get('name', 'N/A')}")
            sections.append(f"Email: {info.get('email', 'N/A')}")
            sections.append(f"Location: {info.get('location', 'N/A')}")
        
        if 'summary' in resume_data:
            sections.append(f"Summary: {resume_data['summary']}")
        
        if 'skills' in resume_data:
            skills = ', '.join(resume_data['skills']) if isinstance(resume_data['skills'], list) else resume_data['skills']
            sections.append(f"Skills: {skills}")
        
        if 'experience' in resume_data:
            sections.append("Experience:")
            for exp in resume_data.get('experience', []):
                sections.append(f"- {exp.get('title', '')} at {exp.get('company', '')}")
                sections.append(f"  {exp.get('duration', '')}")
                sections.append(f"  {exp.get('description', '')}")
        
        if 'education' in resume_data:
            sections.append("Education:")
            for edu in resume_data.get('education', []):
                sections.append(f"- {edu.get('degree', '')} from {edu.get('institution', '')}")
                sections.append(f"  {edu.get('year', '')}")
        
        if 'raw_text' in resume_data:
            sections.append(resume_data['raw_text'])
        
        return '\n'.join(sections)
    
    def _prepare_job_description(self, job_data: Dict[str, Any]) -> str:
        sections = []
        
        sections.append(f"Job Title: {job_data.get('title', 'N/A')}")
        sections.append(f"Company: {job_data.get('company', 'N/A')}")
        sections.append(f"Location: {job_data.get('location', 'N/A')}")
        
        if 'description' in job_data:
            sections.append(f"Description: {job_data['description']}")
        
        if 'requirements' in job_data:
            reqs = job_data['requirements']
            if isinstance(reqs, list):
                sections.append("Requirements:")
                for req in reqs:
                    sections.append(f"- {req}")
            else:
                sections.append(f"Requirements: {reqs}")
        
        if 'preferred_qualifications' in job_data:
            sections.append(f"Preferred: {job_data['preferred_qualifications']}")
        
        if 'salary_range' in job_data:
            sections.append(f"Salary: {job_data['salary_range']}")
        
        return '\n'.join(sections)
    
    def _enhance_analysis(self, llm_analysis: Dict[str, Any], resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        enhanced = llm_analysis.copy()
        
        location_score = self._calculate_location_match(
            resume_data.get('personal_info', {}).get('location', ''),
            job_data.get('location', '')
        )
        enhanced['location_match'] = location_score
        
        if enhanced.get('overall_score', 0) == 0:
            enhanced['overall_score'] = self._calculate_weighted_score(enhanced)
        
        if not enhanced.get('recommendations'):
            enhanced['recommendations'] = self._generate_recommendations(enhanced)
        
        return enhanced
    
    def _calculate_location_match(self, resume_location: str, job_location: str) -> int:
        if not resume_location or not job_location:
            return 50
        
        resume_loc_lower = resume_location.lower()
        job_loc_lower = job_location.lower()
        
        if resume_loc_lower == job_loc_lower:
            return 100
        
        if 'remote' in job_loc_lower or 'anywhere' in job_loc_lower:
            return 100
        
        if any(loc in resume_loc_lower for loc in job_loc_lower.split()):
            return 80
        
        if any(loc in job_loc_lower for loc in resume_loc_lower.split()):
            return 70
        
        same_country_indicators = ['usa', 'united states', 'us', 'india', 'uk', 'canada']
        for indicator in same_country_indicators:
            if indicator in resume_loc_lower and indicator in job_loc_lower:
                return 60
        
        return 30
    
    def _calculate_weighted_score(self, analysis: Dict[str, Any]) -> float:
        skill_score = len(analysis.get('matched_skills', [])) * 10
        skill_score = min(100, skill_score)
        
        exp_score = analysis.get('experience_match', 50)
        edu_score = analysis.get('education_match', 50)
        loc_score = analysis.get('location_match', 50)
        
        keyword_score = 70 if analysis.get('matched_skills') else 30
        
        weighted_score = (
            skill_score * self.weight_config['skills'] +
            exp_score * self.weight_config['experience'] +
            edu_score * self.weight_config['education'] +
            loc_score * self.weight_config['location'] +
            keyword_score * self.weight_config['keywords']
        )
        
        return min(100, max(0, int(weighted_score)))
    
    def _calculate_breakdown(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'skills_score': min(100, len(analysis.get('matched_skills', [])) * 10),
            'experience_score': analysis.get('experience_match', 0),
            'education_score': analysis.get('education_match', 0),
            'location_score': analysis.get('location_match', 0),
            'weights': self.weight_config
        }
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        recommendations = []
        
        skill_gaps = analysis.get('skill_gaps', [])
        if skill_gaps:
            top_skills = skill_gaps[:3]
            recommendations.append(f"Consider acquiring skills in: {', '.join(top_skills)}")
        
        if analysis.get('experience_match', 0) < 60:
            recommendations.append("Gain more relevant experience through projects or internships")
        
        if analysis.get('education_match', 0) < 60:
            recommendations.append("Consider relevant certifications or courses to strengthen your profile")
        
        if analysis.get('location_match', 0) < 50:
            recommendations.append("Consider relocation or remote work options")
        
        if analysis.get('overall_score', 0) >= 80:
            recommendations.append("Strong match! Tailor your cover letter to highlight matched skills")
        elif analysis.get('overall_score', 0) >= 60:
            recommendations.append("Good potential match. Emphasize transferable skills in your application")
        else:
            recommendations.append("Consider building more relevant experience before applying")
        
        return recommendations
    
    def _create_fallback_result(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        resume_skills = set()
        if 'skills' in resume_data:
            if isinstance(resume_data['skills'], list):
                resume_skills = set(s.lower() for s in resume_data['skills'])
            else:
                resume_skills = set(resume_data['skills'].lower().split(','))
        
        job_text = ' '.join([
            job_data.get('title', ''),
            job_data.get('description', ''),
            str(job_data.get('requirements', ''))
        ]).lower()
        
        matched_skills = [skill for skill in resume_skills if skill in job_text]
        
        basic_score = min(100, len(matched_skills) * 15 + 30)
        
        return {
            'overall_score': basic_score,
            'matched_skills': matched_skills,
            'skill_gaps': [],
            'transferable_skills': [],
            'experience_match': 50,
            'education_match': 50,
            'location_match': 50,
            'recommendations': ["Unable to perform detailed analysis. Please try again."],
            'calculated_at': datetime.utcnow().isoformat(),
            'scoring_breakdown': {
                'skills_score': len(matched_skills) * 15,
                'experience_score': 50,
                'education_score': 50,
                'location_score': 50,
                'weights': self.weight_config
            }
        }