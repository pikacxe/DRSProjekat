import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Currency } from '../interfaces/currency-interface';

@Injectable({
  providedIn: 'root',
})
export class CurrencyRatesService {
  private _currency_rates$ = new BehaviorSubject<Currency[]>([]);
  public currency_rates$ = this._currency_rates$.asObservable();

  setCurrencyRates(new_rates: Currency[]) {
    this._currency_rates$.next(new_rates);
  }

  constructor() {}
}
