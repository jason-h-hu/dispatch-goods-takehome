import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  url: string = 'http://127.0.0.1:8000';
  selectedFile: File | undefined;
  ids: string[] = [];

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  onSubmit(event: any) {
    event.preventDefault();
    if (this.selectedFile) {
      const uploadData = new FormData();
      uploadData.append('file', this.selectedFile, this.selectedFile.name);
      this.http.post(this.url, uploadData).subscribe(
        (response) => {
          console.log('File uploaded successfully:', response);
          this.ids = (response as any).ids as string[]; // Assuming the response contains an array of IDs
        },
        (error) => {
          console.error('Error uploading file:', error);
        }
      );
    }
  }
}
