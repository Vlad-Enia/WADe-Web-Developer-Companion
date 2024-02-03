
import { HttpClient, HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest, HttpResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Router } from "@angular/router";
import { throwError } from "rxjs";
import { catchError, map } from "rxjs/operators";
import { AuthService } from "./auth.service";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private http: HttpClient, private auth: AuthService, private router: Router) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): any {

    const authorization = this.auth.authorization;

    if (authorization) {
      request = request.clone({
        setHeaders: {
          Authorization: `${authorization.token_type} ${authorization.access_token}`
        }
      })
    }

    return next.handle(request).pipe(
      map((event: HttpEvent<any>) => event),
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          if (error.error.error === 'invalid_token') {
            this.auth.refresh(authorization).subscribe(
                () => location.reload(),
                () => this.router.navigate(['login'])
            );
          } else {
            this.router.navigate(['login']);
          }
        }
        return throwError(error);
      })
    );
  }
}
