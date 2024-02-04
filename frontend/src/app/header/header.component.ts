import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Router } from '@angular/router';
import { AuthService } from '../service/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {

  title = "WDC";

  constructor(private router: Router, private auth: AuthService) {
  }

  logout(): void {
    this.auth.forget()
    this.router.navigate(['login']);
  }
}
