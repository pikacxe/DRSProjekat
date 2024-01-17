import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {

  constructor(
    private http:HttpClient
  ) { }

  getCurrencyRates() {
    return this.http.get<any>('https://kurs.resenje.org/api/v1/rates/today');
  }
}
