package com.example.parser_api;

import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("api/v1/resumes")
@AllArgsConstructor
public class ResumeController {
    private final ResumeService resumeService;

    @GetMapping
    public List<Resume> fetchAllResumes(){
        return resumeService.getAllResumes();
    }

    @PostMapping
    public String insertResume(@RequestBody Resume resume){
        return resumeService.insertMyResume(resume);
    }
}
