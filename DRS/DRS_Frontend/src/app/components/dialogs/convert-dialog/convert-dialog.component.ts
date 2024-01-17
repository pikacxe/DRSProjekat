import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Currency } from '../../../interfaces/currency-interface';
import { CurrencyRatesService } from '../../../services/currency-rates.service';

@Component({
  selector: 'app-convert-dialog',
  templateUrl: './convert-dialog.component.html',
  styleUrl: './convert-dialog.component.scss',
})
export class ConvertDialogComponent implements OnInit {
  selectedValue = '';
  currencies: Currency[] = [];
  balanceInRsd: number;
  balanceToShow: any;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private ratesService: CurrencyRatesService
  ) {}

  ngOnInit(): void {
    this.ratesService.currency_rates$.subscribe({
      next: (res) => {
        this.currencies = res;
      },
    });
    this.selectedValue = this.data.balance.currency;
    this.balanceToShow = this.data.balance.balance;
    var selectedCurrency = this.currencies.find(
      (currency) => currency.currency == this.selectedValue
    );
    console.log(selectedCurrency);
    var selectedCurrencyExchange;
    if (selectedCurrency) {
      selectedCurrencyExchange = selectedCurrency.exchange;
      console.log(selectedCurrencyExchange);
    }
    if (selectedCurrencyExchange) {
      this.balanceInRsd = this.data.balance.balance * selectedCurrencyExchange;
      console.log(this.balanceInRsd);
    }
  }

  calculateBalance() {
    let selectedCurrency = this.currencies.find(
      (currency) => currency.currency === this.selectedValue
    );
    if (selectedCurrency) {
      this.balanceToShow = this.balanceInRsd;
      this.balanceToShow = (
        this.balanceToShow / selectedCurrency.exchange
      ).toFixed(2);
    }
  }
}
