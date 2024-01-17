import { Component, OnInit } from '@angular/core';
import { SocketService } from '../../services/socket.service';
import { MatTableDataSource } from '@angular/material/table';
import { LoadingService } from '../../services/loading.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-main-page-admin',
  templateUrl: './main-page-admin.component.html',
  styleUrl: './main-page-admin.component.scss'
})
export class MainPageAdminComponent implements OnInit{
  isLonger = false;
  transactions: any[] = [];
  transactionsDataSource: MatTableDataSource<any>;
  displayedColumns: string[] = ['id', 'amount', 'currency', 'created', 'completed', 'recipientName', 'recipientCardNumber', 'recipientEmail', 'senderCardNumber', 'state'];
  constructor(
    private socketService: SocketService,
    private loadingService: LoadingService,
  ) {}

  ngOnInit(): void {
    this.loadingService.setLoadingState(true);
    this.socketService.listen('transaction_processing')
    .subscribe({
      next: (res) => {
        console.log(res);
        if(res.length > 9) {
          this.isLonger = true;
        }
        let data = res.map((response: any) => ({
          ...response,
          recipient_name: response.recipient_first_name + ' ' + response.recipient_last_name,
        }));
        this.transactionsDataSource = new MatTableDataSource(data);
        this.loadingService.setLoadingState(false);
      }
    })
  }

}
