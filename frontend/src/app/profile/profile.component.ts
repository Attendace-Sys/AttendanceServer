import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup} from '@angular/forms';
import {UploadService} from '../services/upload_services/upload.service';
import {NotificationService} from '../services/notification_services/notification.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss' ]
})
export class ProfileComponent implements OnInit {

  DJANGO_SERVER = 'http://127.0.0.1:8000';
  form: FormGroup;
  myFiles: string[] = [];
  response;
  imageURL = './../../assets/error.png' ;

  constructor(
    private formBuilder: FormBuilder,
    private uploadService: UploadService,
    private notificationService: NotificationService
    ) { }

  ngOnInit() {
    this.form = this.formBuilder.group({
      fileName: '',
      studentName: '',
      studentCode: '',
      studentClass: '',
      fileData: []
    });
  }
  get fileData() { return this.form.get('fileData'); }
  get fileName() { return this.form.get('fileName'); }
  get studentName() { return this.form.get('studentName'); }
  get studentCode() { return this.form.get('studentCode'); }
  get studentClass() { return this.form.get('studentClass'); }

  onChange(event) {
    if (event.target.files.length > 0) {
      // tslint:disable-next-line:prefer-for-of
      for (let i = 0; i < event.target.files.length; i++) {
          this.myFiles.push(event.target.files[i]);
      }
    }
  }

  onSubmit() {
    const formData = new FormData();
    // tslint:disable-next-line:prefer-for-of
    for (let i = 0; i < this.myFiles.length; i++ ) {
      formData.append('file_data', this.myFiles[i]);
      const fName = this.fileName.value + '[' + i + ']' + '.png';
      formData.set('file_data', this.myFiles[i], fName);
    }
    formData.append('file_name', this.fileName.value );
    formData.append('student_name', this.studentName.value );
    formData.append('student_code', this.studentCode.value );
    formData.append('student_class', this.studentClass.value );
    this.notificationService.showLoading();
    this.uploadService.upload(formData).subscribe(
      (res) => {
        this.response = res;
        // this.imageURL = `${this.DJANGO_SERVER}${res.file}`;
        this.notificationService.success(this.imageURL);
      },
      (err) => {
        this.notificationService.error(err.statusText);
      }
    );
  }
}
