package com.example.parser_api;

import org.springframework.data.mongodb.repository.MongoRepository;

import javax.swing.text.html.Option;
import java.util.Optional;

public interface ResumeRepository extends MongoRepository<Resume,String> {
}
