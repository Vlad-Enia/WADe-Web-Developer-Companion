import { Component } from '@angular/core';
import { Router } from "@angular/router";
import { AuthService } from '../service/auth.service';

@Component({
  selector: 'main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent {

  

  constructor(private router: Router, private auth: AuthService) {
  }

  logout(): void {
    this.router.navigate(['login']);
  }

}
