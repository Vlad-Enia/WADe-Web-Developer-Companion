import { Component } from '@angular/core';
import { Router } from "@angular/router";

@Component({
  selector: 'main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent {

  

  constructor( private router: Router) {
  }

  logout(): void {
    this.router.navigate(['login']);
  }

}
