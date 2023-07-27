import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { FormRoutingModule } from './form-routing.module';
import { BasicInfoComponent } from './basic-info/basic-info.component';
import { EducationalBackgroundComponent } from './educational-background/educational-background.component';
import { ProfessionalExperienceComponent } from './professional-experience/professional-experience.component';
import { ResumeComponent } from './resume/resume.component';


@NgModule({
  declarations: [
    BasicInfoComponent,
    EducationalBackgroundComponent,
    ProfessionalExperienceComponent,
    ResumeComponent
  ],
  imports: [
    CommonModule,
    FormRoutingModule,
    ReactiveFormsModule,
    FormRoutingModule
  ]  
})
export class FormModule { }
