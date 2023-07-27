import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BasicInfoComponent } from './basic-info/basic-info.component';
import { EducationalBackgroundComponent } from './educational-background/educational-background.component';
import { ProfessionalExperienceComponent } from './professional-experience/professional-experience.component';
import { ResumeComponent } from './resume/resume.component';

const routes: Routes = [
  { path: 'basic-info', component: BasicInfoComponent },
  { path: 'educational-background', component: EducationalBackgroundComponent },
  { path: 'professional-experience', component: ProfessionalExperienceComponent },
  { path: 'resume', component: ResumeComponent },
  { path: '', redirectTo: 'basic-info', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FormRoutingModule { }
