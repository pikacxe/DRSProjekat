import {
  HttpClient,
  HttpHeaders,
  HttpParams,
  HttpUrlEncodingCodec,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { HotToastService } from '@ngneat/hot-toast';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private http: HttpClient,
    private jwt: JwtHelperService,
    private toaster: HotToastService
  ) {}

  setToken(token: string) {
    localStorage.setItem('access-token', token);
  }
  getToken() {
    return localStorage.getItem('access-token');
  }

  logIn(data: any) {
    const body = new HttpParams({ encoder: new HttpUrlEncodingCodec() })
      .set('email', data.email)
      .set('password', data.password);

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/x-www-form-urlencoded',
      }),
    };

    
    const url = environment.baseURL + '/login';
    console.log(url);
    return this.http.post<any>(url, body, httpOptions);
  }

  isTokenValid(token: string | null = this.getToken()): boolean {
    if (!token || this.jwt.isTokenExpired(token)) {
      this.toaster.info('Please log in again');
      this.logOut();
      return false;
    }
    return true;
  }

  logOut() {
    localStorage.clear();
  }
}
