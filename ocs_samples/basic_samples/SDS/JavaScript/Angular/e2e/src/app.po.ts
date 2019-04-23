import { browser, by, element, protractor } from 'protractor';
import cred from './cred.json';

export class AppPage {
    writeScreenShot(data, filename) {
        const fs = require('fs');
        const stream = fs.createWriteStream(filename);
        stream.write(new Buffer(data, 'base64'));
        stream.end();
    }

    helper(path: string, expectation: string): any {
        return element(by.id(path)).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.id(path + 'Message')).getText()
                    .then((txt) => {
                        expect(txt).toContain(expectation);
                    });
            });
/*#createType
        return element(by.xpath('//*[@id="' + path + '"]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('//*[@id="' + path + 'Message"]')).getText()
                    .then((txt) => {
                        expect(txt).toContain(expectation);
                    });
            });
            */
    }
    createType(): any {        
        console.log('create type');
        element(by.xpath('/html')).getText().then((res) => {
            console.log(res);
        })
        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/div/button')).click()
        .then((res) => {
            browser.driver.sleep(2000);
            element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/div/span')).getText()
                .then((txt) => {
                    expect(txt).toContain("201");
                });
        });
        // return this.helper('createType', '201');
    }

    createStream(): any {
        return this.helper('createStream', '201');
    }

    writeData(): any {
        return this.helper('writeWaveDataEvents', '204');
    }

    retreiveEvents(): any {
        return this.helper('retrieveWaveDataEvents', '10 events');
    }

    // todo update this
    retrieveWaveDataEventsHeaders(): any {
        return this.helper('retrieveWaveDataEventsHeaders', '');
    }

    updateValues(): any {
        return this.helper('updateWaveDataEvents', '204');
    }

    replaceValues(): any {
        return this.helper('replaceWaveDataEvents', '204');
    }

    // todo update this
    retrieveInterpolatedValues(): any {
        return this.helper('retrieveInterpolatedValues', '');
    }

    // todo update this
    retrieveFilteredValues(): any {
        return this.helper('retrieveFilteredValues', '');
    }

    propertyOverride(): any {
        return this.helper('createPropertyOverrideAndUpdateStream', '204');
    }

    createSdsType2(): any {
        return this.helper('createAutoStreamViewTargetType', '201');
    }

    createSdsStream2(): any {
        return this.helper('createAutoStreamView', '201');
    }

    retreiveEventsBasedOnSdsView(): any {
        return this.helper('retrieveWaveDataEventsAutoStreamView', '');
    }

    createStreamViewWithProps(): any {
        return this.helper('createSdsStreamViewPropertiesAndManualType', '201');
    }

    getEvents2(): any {
        return this.helper('retrieveWaveDataEventsManualStreamView', '');
/*
        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[11]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/div[3]/table/tbody/tr[1]/th[1]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("OrderTarget");
                    });
            });
*/
    }

    sdsStreamViewMap(): any {
        return this.helper('getSdsStreamViewMap', '');

//        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[12]')).click();
    }

    updateStreamType(): any {
        return this.helper('updateStreamType', '');
    }

    filterTypes(): any {
        return this.helper('filterTypes', '');
    }

    createTagsAndMetaData(): any {
        return this.helper('createTagsAndMetadata', '200');
    }


    getTags(): any {
        return this.helper('getAndPrintTags', '');

        /*
        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[14]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/span[14]')).getText()
                    .then((txt) => {
                        expect(txt).toContain("waves, periodic, 2018, validated");
                    });
            });
            */
    }

    getMetadata(): any {
        return this.helper('getAndPrintMetadata', '');

        /*
        return element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/button[15]')).click()
            .then((res) => {
                browser.driver.sleep(2000);
                element(by.xpath('/html/body/app-root/div/div/div/div/app-datasrc/div/div[6]/table/tbody/tr[4]/td[1]')).getText()
                    .then((txt) => {
                       // expect(txt).toContain("Province");
                    });
            });
            */
    }


    deleteVal(): any {
        return this.helper('deleteAllValues', '204');
    }

    secondaryCreate(): any {
        return this.helper('secondaryCreate', '');
    }

    secondaryUpdate(): any {
        return this.helper('secondaryUpdate', '');
    }

    secondaryDelete(): any {
        return this.helper('secondaryDelete', '');
    }

    createCompoundTypeandStream(): any {
        return this.helper('createCompoundTypeandStream', '');
    }

    createAndRetreiveCompoundData(): any {
        return this.helper('createAndRetreiveCompoundData', '');
    }

    deleteRest(): any {
        return this.helper('cleanup', 'All Objects Deleted');
    }



  navigateTo() {
    return browser.get(browser.baseUrl) as Promise<any>;
  }

  getTitleText() {
    return element(by.css('app-root h1')).getText() as Promise<string>;
  }

    login2() {
   
        element(by.xpath('/html')).getText().then((res) => {
            console.log('login');
            console.log(res);
        })
        return element(by.xpath('/html/body/app-root/nav/div/a[2]')).click()
            .then((res) => {
                browser.driver.sleep(3000)
                    .then((res) => {
                        element(by.xpath('/html')).getText().then((res) => {
                            console.log('choices');
                            console.log(res);
                        })
                        browser.driver.findElement(by.xpath('/html/body/div[3]/div/div[2]/a[1]'))
                            .then((ele) => {
                                ele.click()
                                .then((res) => {
                                    browser.driver.sleep(3000)
                                    .then((res) => {
                                        this.loginWithGoogle(cred.login, cred.pass);
                                    });
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
                element(by.xpath('/html')).getText().then((res) => {
                    console.log('email');
                    console.log(res);
                })
                el.sendKeys(username + protractor.Key.ENTER) ;
            }).then(() => {
                browser.driver.sleep(4000);
            }).then(() => {        
                element(by.xpath('/html')).getText().then((res) => {
                    console.log('password');
                    console.log(res);
                })
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
