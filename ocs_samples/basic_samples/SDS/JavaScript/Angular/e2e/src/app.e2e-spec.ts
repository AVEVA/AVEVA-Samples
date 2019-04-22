import { AppPage } from './app.po';
import { browser, logging } from 'protractor';

describe('workspace-project App', () => {
    let page: AppPage;
    var originalTimeout;

    beforeEach((done) => {
      originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
      jasmine.DEFAULT_TIMEOUT_INTERVAL = 1000000;
      page = new AppPage();
      done();
  });

  it('should just work...', (done) => {
      browser.waitForAngularEnabled(false); 
      page.navigateTo()
          .then((res) => {
              page.login2()
                  .then((res) => {
                      browser.driver.sleep(10000)
                          .then((res) => {
                              page.createType()
                                  .then((res) => {
                                      page.createStream()
                                          .then((res) => {
                                              page.writeData()
                                                  .then((res) => {
                                                      page.retreiveEvents()
                                                          .then((res) => {
                                                              page.updateValues()
                                                                  .then((res) => {
                                                                      page.replaceValues()
                                                                          .then((res) => {
                                                                              page.propertyOverride()
                                                                                  .then((res) => {
                                                                                      page.createSdsType2()
                                                                                          .then((res) => {
                                                                                              page.createSdsStream2()
                                                                                                  .then((res) => {
              page.retreiveEventsBasedOnSdsView()
                  .then((res) => {
                      page.createStreamViewWithProps()
                          .then((res) => {
                              page.getEvents2()
                                  .then((res) => {
                                      page.sdsStreamViewMap()
                                          .then((res) => {
                                              page.createTagsAndMetaData()
                                                  .then((res) => {
                                                      page.getTags()
                                                          .then((res) => {
                                                              page.getMetadata()
                                                                  .then((res) => {
                                                                      page.deleteVal()
                                                                          .then((res) => {
                                                                              page.deleteRest()
                                                                                  .then((res) => {
                                                                                      done();
                                                                                  });
                                                                          });
                                                                  });
                                                          });
                                                  });
                                          });
                                  });
                          });
                  });
                  });
                                                                                      });
                                                                                  });
                                                                          });
                                                                  });
                                                          });
                                                  });
                                          });
                                  });
                          });
                  });
          })

  });

    afterEach((done) => {

        //page.deleteRest();
    // Assert that there are no errors emitted from the browser
    /*
     * const logs = browser.manage().logs().get(logging.Type.BROWSER);
    expect(logs).not.toContain(jasmine.objectContaining({
      level: logging.Level.SEVERE,
    } as logging.Entry));
    */
        jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
        done();
    });

    afterAll((done) => {

        page.deleteRest();
        done();
    });
});
