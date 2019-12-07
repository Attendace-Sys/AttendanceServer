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

  DJANGO_SERVER = 'http://127.0.0.1:8000/students/';
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
      student_code: '',
      first_name: '',
      last_name: '',
      email: '',
      username: '',
      password: '',
      students_video_data: '',
      files: []
    });
  }
  get student_code() { return this.form.get('student_code'); }
  get first_name() { return this.form.get('first_name'); }
  get last_name() { return this.form.get('studelast_namentName'); }
  get email() { return this.form.get('email'); }
  get username() { return this.form.get('username'); }
  get password() { return this.form.get('password'); }
  get students_video_data() { return this.form.get('students_video_data'); }
  get files() { return this.form.get('files'); }

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
