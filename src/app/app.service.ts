import { Injectable } from '@angular/core';
import { Http , Response } from '@angular/http';
import { custDetails } from './page1.model';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';


@Injectable()
export class AppService {
  private endpointUrl = "http://127.0.0.1:5000/";

  constructor(private http: Http) { }

  getCust() {
    fetch(this.endpointUrl).then(Response=>{console.log(Response)});

    //return this.http.get(this.endpointUrl ).map((response: Response) => {const result = response.json();
    //  return result;}).catch((error : Response | any) => {console.log(error.statusText);
    //   return Observable.throw(error.statusText);});
  }

  
  


}
