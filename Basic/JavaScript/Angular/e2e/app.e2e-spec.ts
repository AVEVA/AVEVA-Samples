import { angular6samplePage } from './app.po';

describe('angular6sample App', () => {
  let page: angular6samplePage;

  beforeEach(() => {
    page = new angular6samplePage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
