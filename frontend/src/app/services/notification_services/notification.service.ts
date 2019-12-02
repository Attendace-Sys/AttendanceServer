import { Injectable } from '@angular/core';
import { interval } from 'rxjs';

declare var $: any;

@Injectable({
    providedIn: 'root'
})
export class NotificationService {
    private _isShow = false;
    private _isError = false;

    private _isShowProgress = true;
    private _progress = 0;
    private _maxProgress = 90;
    private _lastInterval = 0;

    private _message: string = null;

    private _confirmFn: any = null;

    public get isShow(): boolean { return this._isShow; }
    public get isError(): boolean { return this._isError; }

    public get isShowProgress(): boolean { return this._isShowProgress; }
    public get progress(): number { return this._progress; }

    public get message() {
        return this._message;
    }

    constructor() { }

    public showLoading(showProgress: boolean = true, progress: number = 0, successCallback: () => void = null) {
        this._isError = false;
        this._isShow = showProgress;
        this._progress = progress;
        this._maxProgress = 90;
        this._lastInterval = 0;

        this._isShow = true;

        // tslint:disable-next-line:prefer-const
        let updateInterval = interval(50).subscribe(value => {
            if (this.update(value)) {
                updateInterval.unsubscribe();

                if (this._message !== null) {
                    $('#notification-modal').modal('show');

                    $('#notification-modal').on('hidden.bs.modal', function (e) {
                        if (successCallback && this._isError) {
                            successCallback();
                        }
                    });
                } else {
                    this.hideLoading();
                }
            }
        });
    }

    // tslint:disable-next-line:no-shadowed-variable
    update(interval: number): boolean {
        let result = false;

        // tslint:disable-next-line:prefer-const
        let elapsedTime = interval - this._lastInterval;
        this._lastInterval = interval;

        if (this._progress < this._maxProgress) {
            this._progress += elapsedTime * 10;

            if (this._progress > this._maxProgress) {
                this._progress = this._maxProgress;
            }
        } else if (this._progress > this._maxProgress) {
            this._progress = this._maxProgress;
        }

        result = (this._progress >= 100);

        return result;
    }

    hideLoading() {
        this._isShow = false;
    }

    showProgress() {
        this._isShowProgress = true;
    }

    hideProgress() {
        this._isShowProgress = false;
    }

    setMessage(message: string = null, error: boolean = false) {
        this._maxProgress = 100;

        this._message = message;
        this._isError = error;
    }

    success(message: string = null) {
        this.setMessage(message, false);
    }

    error(message: string = null) {
        this.setMessage(message, true);
    }

    showConfirm(confirm: () => void) {
        this._isError = false;

        $('#confirm-modal').modal('show');

        this._confirmFn = confirm;
    }

    invokeConfirmFn() {
        if (this._confirmFn != null) {
            this._confirmFn();

            this._confirmFn = null;

            $('#confirm-modal').modal('hide');
        }
    }
}
