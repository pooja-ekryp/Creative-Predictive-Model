import { AngularFormsAppPage } from './app.po';

describe('angular-forms-app App', function() {
  let page: AngularFormsAppPage;

  beforeEach(() => {
    page = new AngularFormsAppPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
