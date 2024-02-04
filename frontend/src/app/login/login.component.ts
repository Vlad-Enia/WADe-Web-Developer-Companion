import { HttpErrorResponse } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../service/auth.service';
import { HttpClient } from "@angular/common/http";
import { environment } from "src/environments/environment";


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

  constructor(private router: Router, private auth: AuthService, private http: HttpClient) {
    this.username = ''
    this.password = ''
  }

  login(): void {
    this.auth.authorize(this.username, this.password).subscribe(
      () => {
        this.error = false;
        this.status = '';
        this.date = '';
        this.router.navigate(['main']);
        const url = `${environment.backendBaseUrl}/main`
        this.http.get(url).subscribe(data => {
          console.log(data)
        })
      },
      (error: HttpErrorResponse) => {
        this.error = true;
        this.status = error.status.toString();
        this.date = new Date().toISOString();
        this.router.navigate(['login']);
      }
    );
  }

}
