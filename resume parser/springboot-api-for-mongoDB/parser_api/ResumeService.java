package com.example.parser_api;

import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@AllArgsConstructor
@Service
public class ResumeService {
    @Autowired
    private final ResumeRepository resumeRepository;
    public List<Resume> getAllResumes(){
        return resumeRepository.findAll();
    }
    public String insertMyResume(Resume resume) {
        Resume savedResume = resumeRepository.insert(resume);
        if (savedResume != null) {
            return "successful";
        } else {
            return "failed";
        }
    }
}
