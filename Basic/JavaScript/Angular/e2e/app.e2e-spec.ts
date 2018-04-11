import { Angular4samplePage } from './app.po';

describe('angular4sample App', () => {
  let page: Angular4samplePage;

  beforeEach(() => {
    page = new Angular4samplePage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
