import { browser, by, element, protractor } from 'protractor';
//import { Cred } from './app.cred';
import cred from './cred.json';

export class AppPage {
    
    createType(): any {
        
        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/div/button')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/div/span')).getText()
                    .then((txt) => {
                        expect(txt).toContain("201");
                    });
            });        
    }

    createStream(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[1]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[1]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("201");
                    });
            });
    }

    writeData(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[2]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[2]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("204");
                    });
            });
    }

    retreiveEvents(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[3]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[3]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("10 events");
                    });
            });
    }

    updateValues(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[4]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[4]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("204");
                    });
            });
    }

    replaceValues(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[5]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[5]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("204","Failed to find replaceValues");
                    });
            });
    }

    propertyOverride(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[6]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[6]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("204");
                    });
            });
    }

    createSdsType2(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[7]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[7]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("201");
                    });
            });
    }

    createSdsStream2(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[8]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[8]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("201");
                    });
            });
    }

    retreiveEventsBasedOnSdsView(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[9]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/div[2]/table/tbody/tr[1]/th[2]')).getText()
                    .then((txt) => {
                       // expect(txt).toContain("RadiansTarget");
                    });
            });
    }

    createStreamViewWithProps(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[10]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[10]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("201");
                    });
            });
    }

    getEvents2(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[11]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/div[3]/table/tbody/tr[1]/th[1]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("OrderTarget");
                    });
            });
    }

    sdsStreamViewMap(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[12]')).click();
    }

    createTagsAndMetaData(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[13]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[13]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("200");
                    });
            });
    }


    getTags(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[14]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[14]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("waves, periodic, 2018, validated");
                    });
            });
    }

    getMetadata(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[15]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/div[6]/table/tbody/tr[4]/td[1]')).getText()
                    .then((txt) => {
                       // expect(txt).toContain("Province");
                    });
            });
    }


    deleteVal(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[16]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[15]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("204");
                    });
            });
    }

    deleteRest(): any {

        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[17]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[16]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("All Objects Deleted");
                    });
            });
    }



  navigateTo() {
    return browser.get(browser.baseUrl) as Promise<any>;
  }

  getTitleText() {
    return element(by.css('app-root h1')).getText() as Promise<string>;
  }

    login2() {

        return element(by.xpath('/html/body/app-root/nav/div/a[2]')).click()
            .then((res) => {
                browser.driver.sleep(3000)
                    .then((res) => {
                        browser.driver.findElement(by.xpath('/html/body/div[3]/div/div[2]/a[1]'))
                            .then((ele) => {
                                ele.click()
                                    .then((res) => {
                                        this.loginWithGoogle(cred.login, cred.pass);
                                    });
                            });
                    });
            });
    }
/**
* Uses the dreaded `sleep` method because finding the password 
* by any css selector tried fails.
* @param {string} username - A Google username.
* @param {string} passphrase - A Google passpharse.
* @return {Promise.<void>} Promise resolved when logged in.
*/
 loginWithGoogle (username, passphrase) {
    return this.selectWindow(0).then(() => {
        return browser.driver.findElement(by.css('[type="email"]'))
            .then((el) => {
                el.sendKeys(username + protractor.Key.ENTER) ;
            }).then(() => {
                browser.driver.sleep(3000);
            }).then(() => {
                browser.actions().sendKeys(passphrase + protractor.Key.ENTER).perform();
            });
    })
}

/**
* Focus the browser to the specified  window.
* [Implementation by and thanks to]{@link http://stackoverflow.com/questions/21700162/protractor-e2e-testing-error-object-object-object-has-no-method-getwindowha}
* @param  {Number} index The 0-based index of the window (eg 0=main, 1=popup)
* @return {webdriver.promise.Promise.<void>} Promise resolved when the index window is focused.
*/
 selectWindow (index)  {
    browser.driver.wait(function () {
        return browser.driver.getAllWindowHandles().then((handles) => {
            if (handles.length > index) {
                return true;
            }
        });
    });

    return browser.driver.getAllWindowHandles().then((handles) => {
        return browser.driver.switchTo().window(handles[index]);
    });
};
}
