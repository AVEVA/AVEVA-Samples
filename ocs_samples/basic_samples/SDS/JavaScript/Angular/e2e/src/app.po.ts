import { browser, by, element, protractor } from 'protractor';
import cred from './cred.json';

export class AppPage {
    /*writeScreenShot(data, filename) {
        const fs = require('fs');
        const stream = fs.createWriteStream(filename);
        stream.write(new Buffer(data, 'base64'));
        stream.end();
    }*/ // excess debugging

    helper(path: string, expectation: string): any {
        return element(by.id(path)).click()
            .then((res) => {
                browser.driver.sleep(2500);
                element(by.id(path + 'Message')).getText()
                    .then((txt) => {
                        expect(txt).toContain(expectation);
                    });
            });
    }

    createType(): any {
        return this.helper('createType', '20');
    }

    createStream(): any {
        return this.helper('createStream', '20');
    }

    writeData(): any {
        return this.helper('writeWaveDataEvents', '20');
    }

    retreiveEvents(): any {
        return this.helper('retrieveWaveDataEvents', '10 events');
    }

    // todo update this
    retrieveWaveDataEventsHeaders(): any {
        return this.helper('retrieveWaveDataEventsHeaders', '');
    }

    updateValues(): any {
        return this.helper('updateWaveDataEvents', '20');
    }

    replaceValues(): any {
        return this.helper('replaceWaveDataEvents', '20');
    }

    // todo update this
    retrieveInterpolatedValues(): any {
        return this.helper('retrieveInterpolatedValues', '');
    }

    // todo update this
    retrieveFilteredValues(): any {
        return this.helper('retrieveFilteredValues', '');
    }

    // todo update this
    retrieveSampledValues(): any {
        return this.helper('retrieveSampledValues', '');
    }

    propertyOverride(): any {
        return this.helper('createPropertyOverrideAndUpdateStream', '20');
    }

    createSdsType2(): any {
        return this.helper('createAutoStreamViewTargetType', '20');
    }

    createSdsStream2(): any {
        return this.helper('createAutoStreamView', '20');
    }

    retreiveEventsBasedOnSdsView(): any {
        return this.helper('retrieveWaveDataEventsAutoStreamView', '');
    }

    createStreamViewWithProps(): any {
        return this.helper('createSdsStreamViewPropertiesAndManualType', '20');
    }

    getEvents2(): any {
        return this.helper('retrieveWaveDataEventsManualStreamView', '');
    }

    sdsStreamViewMap(): any {
        return this.helper('getSdsStreamViewMap', '');
    }

    updateStreamType(): any {
        return this.helper('updateStreamType', '');
    }

    queryTypes(): any {
        return this.helper('queryTypes', '');
    }

    createTagsAndMetaData(): any {
        return this.helper('createTagsAndMetadata', '20');
    }

    getTags(): any {
        return this.helper('getAndPrintTags', '');
    }

    getMetadata(): any {
        return this.helper('getAndPrintMetadata', '');
    }


    deleteVal(): any {
        return this.helper('deleteAllValues', '20');
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
        return this.helper('cleanup', '');
    }



  navigateTo() {
    return browser.get(browser.baseUrl) as Promise<any>;
  }

  getTitleText() {
    return element(by.css('app-root h1')).getText() as Promise<string>;
  }

    login2() {
   
        /*element(by.xpath('/html')).getText().then((res) => {
            console.log('!!login');
            console.log(res);
        })*/ // excess debugging
        return element(by.xpath('/html/body/app-root/nav/div/a[2]')).click()
            .then((res) => {
                browser.driver.sleep(3000)
                    .then((res) => {
                        /*element(by.xpath('/html')).getText().then((res) => {
                            console.log('!!choices');
                            console.log(res);
                        })*/ // excess debugging
                        browser.driver.findElement(by.css('a.osi-provider:nth-child(5)'))
                            .then((ele) => {
                                ele.click()
                                .then((res) => {
                                    browser.driver.sleep(3000)
                                    .then((res) => {
                                        this.loginWithOutlook(cred.login, cred.pass);
                                        //this.loginWithGoogle(cred.login, cred.pass);
                                    });
                                });
                            });
                    });
            });
    }
    
    loginWithOutlook (username, passphrase) {
    return this.selectWindow(0).then(() => {
        return browser.driver.findElement(by.xpath('//*[@id="i0116"]')) 
            .then((el) => {                
                /*element(by.xpath('/html')).getText().then((res) => {
                    console.log('!!email');
                    console.log(res);
                    console.log('!@!' + username);
                })*/ // excess debugging
                el.sendKeys(username + protractor.Key.ENTER) ;
            }).then(() => {
                browser.driver.sleep(4000);
            }).then(() => {        
                /*element(by.xpath('/html')).getText().then((res) => {
                    console.log('!!password');
                    console.log(res);
                })*/ // excess debugging
                browser.actions().sendKeys(passphrase + protractor.Key.ENTER).perform();
            });
    })
}

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
