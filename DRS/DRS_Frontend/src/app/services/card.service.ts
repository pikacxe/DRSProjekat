import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

const URL = environment.baseURL + '/card/'

@Injectable({
  providedIn: 'root'
})
export class CardService {

  constructor(
    private http: HttpClient,
  ) { }

  getAllCards(token:string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      })
    }
    return this.http.get<any>(URL, httpOptions);
  }

  addCard(data: any, token:string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      })
    }
    
    return this.http.post<any>(URL+'add', data, httpOptions);
  }

  addFunds(data: any, cardNumber:string, token:string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      })
    }
    
    return this.http.post<any>(URL + cardNumber + '/deposit', data, httpOptions);
  }
}
