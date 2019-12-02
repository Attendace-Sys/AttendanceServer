import { Component, OnInit } from '@angular/core';
import { NotificationService } from '../../services/notification_services/notification.service';

declare var $: any;

@Component({
  selector: 'app-notification, .app-notification, [app-notification]',
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.component.scss']
})
export class NotificationComponent implements OnInit {
  constructor(
    private notificationService: NotificationService
  ) { }

  ngOnInit() {
    // tslint:disable-next-line:prefer-const
    let self = this;
    // tslint:disable-next-line:only-arrow-functions
    $('#notification-modal').on('hidden.bs.modal', function(e) {
      self.notificationService.hideLoading();
    });
  }
}
