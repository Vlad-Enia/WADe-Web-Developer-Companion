import { HttpErrorResponse } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';



@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  title = "Login Form";
  error = false;
  status = '';
  date = '';

  @Input() username: string;
  @Input() password: string;

  constructor(private router: Router) {
    this.username = ''
    this.password = ''
  }

  login(): void {
    this.router.navigate(['main']);
  }

}
