
import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { tap } from "rxjs/operators";
import { Authorization } from '../models/models';

@Injectable()
export class AuthService {

  constructor(private http: HttpClient) {
  }

  get authorization(): Authorization {
    var str = localStorage.getItem('authorization');
    return str != null ? JSON.parse(str) : null;
  }

  set authorization(authorization: Authorization) {
    var str = JSON.stringify(authorization);
    localStorage.setItem('authorization', str);
  }

  authorize(username: string, password: string): Observable<Authorization> {
    this.forget();
    var url = `${environment.occ.backendBaseUrl}${environment.occ.authUrl}`
    url = url + '/token';
    url = url + `&grant_type=${Config.OAUTH_GRANT_TYPE_PASSWORD}`;
    url = url + `&username=${username}`;
    url = url + `&password=${password}`;
    return this.http.post<Authorization>(url, {}).pipe(
      tap((authorization: Authorization) => {
        this.authorization = authorization;
      })
    );
  }

  refresh(authorization: Authorization): Observable<Authorization> {
    this.forget();
    var url = `${environment.occ.backendBaseUrl}${environment.occ.authUrl}`
    url = url + '/token';
    url = url + `&grant_type=${Config.OAUTH_GRANT_TYPE_REFRESH_TOKEN}`;
    url = url + `&refresh_token=${authorization.refresh_token}`;
    return this.http.post<Authorization>(url, {}).pipe(
      tap((update: Authorization) => {
        this.authorization = update;
      })
    );
  }

  forget(): void {
    localStorage.removeItem('authorization');
  }
}
