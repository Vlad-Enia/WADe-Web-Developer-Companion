import { Component } from '@angular/core';
import { Router } from "@angular/router";
import { AuthService } from '../service/auth.service';
import { environment } from 'src/environments/environment';
import { Preference } from '../models/models';
import { ContentService } from '../service/content.content_service';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent {

  

  constructor(private router: Router, private auth: AuthService, private http: HttpClient, private contentService: ContentService) {
  }

  logout(): void {
    this.router.navigate(['login']);
  }


  dataSources = [
    {name: 'reddit', selected: false},
    {name: 'mozilla', selected: false},
    {name: 'github', selected: false},
  ]

  content :any[] = []

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
        this.content = response['items']
        console.log(this.content)
      }
    })
  }

}
