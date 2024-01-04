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

  transactions: any[] = [];
  transactionsDataSource: MatTableDataSource<any>;
  displayedColumns: string[] = ['id', 'amount', 'currency', 'created', 'completed', 'recipientName', 'recipientCardNumber', 'recipientEmail', 'senderCardNumber', 'state'];
  constructor(
    private socketService: SocketService,
    private loadingService: LoadingService,
  ) {}

  ngOnInit(): void {
    this.socketService.listen('transaction_processing')
    .subscribe({
      next: (res) => {
        let data = res.map((response: any) => ({
          ...response,
          recipient_name: response.recipient_first_name + ' ' + response.recipient_last_name,
        }));
        this.transactionsDataSource = new MatTableDataSource(data);
      }
    })
  }

}
