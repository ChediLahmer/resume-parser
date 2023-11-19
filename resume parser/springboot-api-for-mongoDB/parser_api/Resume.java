package com.example.parser_api;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "resume")
public class Resume {
    @Id
    private String Id;
    private String experience;
    private String mail;
    private String major;
    private String name;
    private String projects;
    private String role;
}


