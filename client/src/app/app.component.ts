import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.component.html',
})
export class AppComponent {
  url: string = 'http://127.0.0.1:8000';
  selectedFile: File | undefined;
  qrs: string[] = [];
  errors: string[] = [];

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    this.errors = [];
  }

  onSubmit(event: any) {
    event.preventDefault();
    if (this.selectedFile) {
      this.errors = [];
      const uploadData = new FormData();
      uploadData.append('file', this.selectedFile, this.selectedFile.name);
      this.http.post([this.url, 'api'].join('/'), uploadData).subscribe(
        (response) => {
          const userIds: string[] = (response as any).user_ids || [];
          this.qrs = userIds.map((userId) =>
            [this.url, 'qr', `${userId}.png`].join('/')
          );
        },
        (error) => {
          this.errors =
            'error' in error ? Object.values(error.error) : [error.message];
        }
      );
    }
  }
}
