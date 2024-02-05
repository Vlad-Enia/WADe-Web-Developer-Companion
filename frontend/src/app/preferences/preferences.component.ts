import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Preference } from '../models/models';
import { ContentService } from '../service/content.content_service';


@Component({
  selector: 'app-preferences',
  templateUrl: './preferences.component.html',
  styleUrls: ['./preferences.component.scss']
})
export class PreferencesComponent {

  constructor(private http: HttpClient, private contentService: ContentService) {
  }

  dataSources = [
    {name: 'reddit', selected: false},
    {name: 'mozilla', selected: false},
    {name: 'github', selected: false},
  ]

  currentTopic = {name: "currentTopic", value: ''};
  
  existingTopics = []

  ngOnInit(): void{
    this.getPreferencesForCurrentUser()
  }

  getPreferencesForCurrentUser(){
    this.http.get<Preference>(`${environment.backendBaseUrl}/preferences`).subscribe({
      next: (response: Preference) => {
        for(var respDataSource of response.origins){
          this.dataSources.some(data_source => {
            if(data_source.name == respDataSource){
              data_source.selected = true;
            }
          })
        }
      }
    })
  }

  submitForm(){
    var selected_sources = []
    for (var source of this.dataSources){
      if(source.selected)
        selected_sources.push(source.name)
    }
    this.http.post<any>(`${environment.backendBaseUrl}/preferences`, {'selected_sources': selected_sources}).subscribe({
      next: (response) => {
        this.contentService.setContent(response)
      }
    })
  }
}
