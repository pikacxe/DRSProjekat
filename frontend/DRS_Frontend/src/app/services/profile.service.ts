import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

const URL = environment.backendBaseUrl + '/profile'

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  constructor(
    private htpp: HttpClient,
  ) {}

  getUser(token: string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      })
    }
    return this.htpp.get<any>(URL, httpOptions);
  }

  updateProfile(data: any, token: string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      })
    }

    return this.htpp.post<any>(URL + '/update', data, httpOptions);
  }

  changePassword(data: any, token: string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      })
    }
    return this.htpp.post<any>(URL + '/change-password', data, httpOptions);
  }
}
