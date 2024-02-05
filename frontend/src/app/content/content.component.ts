import { Component } from '@angular/core';
import { ContentService } from '../service/content.content_service';

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.scss']
})
export class ContentComponent {
  constructor(private contentService: ContentService){
    console.log(this.contentService.getContent())
  }
}
