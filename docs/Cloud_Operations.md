# AVEVA Cloud Platform

CONNECT data services ([Cds](https://www.aveva.com/en/products/aveva-pi-system/)) is a highly flexible cloud-based platform that provides a scalable, elastic,
centralized environment to aggregate data for reporting, advanced analytics, and third-party applications. Cds is powered by AVEVA's Sequential Data Store (SDS). In this GitHub repo, we provide samples which will help you get started with the [Cds API](https://ocs-docs.osisoft.com/) against your [Cds instance](https://cloud.osisoft.com/welcome).

If you are interested in other AVEVA samples please see [AVEVA Samples](https://github.com/osisoft/OSI-Samples).

If you are new to our APIs and are looking to get going quickly, the  [Types, Streams, and Retrieving Data](https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/COMMON_ACTIONS.md) samples are good starting points.

The official Cds samples are divided in multiple categories depending on the scenario and problem/task, accessible through the following table. 



<details><summary><a href="https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/AUTHENTICATION.md"><b>Authentication</b></a></summary>
<table align="middle" width="100%">
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-authentication_client_credentials-dotnet">Client Credentials</a>
      </b>
      <br />
      Click for
      <a href="docs/AUTHENTICATION.md"> details </a>
      on this type of authentication
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_client_credentials-dotnet">.NET Libraries</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_client_credentials_simple-dotnet">.NET REST API</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_client_credentials_simple-java">Java</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_client_credentials_simple-nodejs">NodeJS</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_client_credentials_simple-postman">Postman</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_client_credentials_simple-powershell">Powershell</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_client_credentials_simple-python">Python</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_client_credentials_simple-rust">Rust</a>
          </td>
        </tr>
      </table>
    </td>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-authentication_hybrid-dotnet"> Hybrid Flow</a>
      </b>
      <br />
      Click for
      <a href="docs/AUTHENTICATION.md"> details </a>
      on this type of authentication
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_hybrid-dotnet">.NET</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="docs/AUTHENTICATION.md"> Authorization Code + PKCE </a>
      </b>
      <br />
      Click for
      <a href="docs/AUTHENTICATION.md"> details </a>
      on this type of authentication
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_authorization-dotnet">.NET</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_authorization-nodejs">NodeJS</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-authentication_authorization-python">Python</a>
          </td>
        </tr>
      </table>
    </td>
    <td></td>
  </tr>
</table>
</details>

<details><summary><a href="https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/COMMON_ACTIONS.md"><b>Types, Streams, and Retrieving Data</b></a></summary>
<table align="middle" width="100%">
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="docs/SDS_WAVEFORM.md"> Read & Write Data with Custom Index</a>
      </b>
      <br />
      This sample covers CRUD operations against the SDS APIs using a non-time series data type called Waveform to illustrate example use cases. (Recommended starting sample)
      <a href="docs/SDS_WAVEFORM.md"> Details </a>
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-waveform_libraries-dotnet">.NET Libraries</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-waveform_rest_api-dotnet">.NET REST API</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-waveform-java">
              Java
            </a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-waveform-angular">
              Angular
            </a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-waveform-nodejs">
              NodeJS
            </a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-waveform-python">
              Python
            </a>
          </td>
        </tr>
      </table>
    </td>
    <td align="middle" valign="top">
      <b>
        <a href="docs/SDS_TIME_SERIES.md">Read & Write Time-Series Data</a>
      </b>
      <br />
      This is similar to the Custom Index Data sample but instead uses a time-series data type to illustrate example use cases. (Recommended starting sample)
      <a href="docs/SDS_TIME_SERIES.md"> Details </a>
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-time_series-python">
              Python
            </a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-time_series-dotnet">
              .NET
            </a>
          </td>
        </tr>
      </table>
    </td>
    <tr>
    <td align="middle" valign="top">
      <b>
        <a href="docs/PI_TO_ADH_READ_DATA.md"> PI to Cds Read Only Streams </a>
      </b>
      <br />
      Covers how to invoke SDS REST APIs via the sample client libraries to read data from PI to Cds streams ingressed to CONNECT data services.
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-pi-to-adh-read-only-data-dotnet">.NET</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-pi-to-adh-read-only-data-python">Python</a>
          </td>
        </tr>
      </table>
    </td>
    <td></td>
  </tr>
  </tr>
</table>
</details>

<details><summary><a href="https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/DATA_INGRESS.md"><b>Data Ingress</b></a></summary>
<table align="middle" width="100%">
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-omf_ingress-dotnet">OMF Ingress</a>
      </b>
      <br />
      Covers the basic functionality of configuring and using the OMF Ingress
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-omf_ingress-dotnet">
              .NET
            </a>
          </td>
        </tr>
      </table>
    </td>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-bulk_upload-dotnet"> Bulk Upload </a>
      </b>
      <br />
      Demonstrates how to build a Bulk Upload utility that sends SDS objects
      from json files
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-bulk_upload-dotnet">.NET</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-csv_to_adh-dotnet">CSV to Cds</a>
      </b>
      <br />
      Shows how to send a basic csv file to Cds using SDS calls
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-csv_to_adh-dotnet">.NET</a>
          </td>
        </tr>
      </table>
    </td>
    <td></td>
  </tr>
  </table>
</details>
  
<details><summary><a href="https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/VISUALIZATION.md"><b>Visualization</b></a></summary>
<table align="middle" width="100%">
<tr>
  <td align="middle" valign="top">
    <b>
      <a href="https://github.com/osisoft/sample-adh-grafana_backend_plugin-datasource">Grafana</a>
    </b>
    <br />
    Demonstrates how to build a Grafana plugin that retrieves stream data from
    Sequential Data Store
    <br />
    <br />
    <table align="middle">
      <tr>
        <td align="middle">
          <a href="https://github.com/osisoft/sample-adh-grafana_backend_plugin-datasource">NodeJS</a>
        </td>
      </tr>
    </table>
  </td>
  <td align="middle" valign="top" width="50%">
    <b>
      <a href="https://github.com/osisoft/sample-sds-visualization-angular">SDS Visualization</a>
    </b>
    <br />
    This sample demonstrates a basic visualization application that can find and trend values from streams in the Sequential Data Store.
    <br />
    <br />
    <table align="middle">
      <tr>
        <td align="middle">
          <a href="https://github.com/osisoft/sample-sds-visualization-angular">Angular</a>
        </td>
      </tr>
    </table>
  </td>
  </tr>
  <tr>
    <td align="middle" valign="top" width="50%">
      <b>
        <a href="docs/ASSETS.md">Assets</a>
      </b>
      <br />
      These samples highlight basic operations with Assets in Cds, including create, update, data retrieval, and delete operations on Assets.
      <a href="docs/ASSETS.md"> Details </a>
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-assets_rest_api-dotnet">.NET</a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-assets-python">Python</a>
          </td>
        </tr>
      </table>
    </td>
    <td align="middle" valign="top" width="50%">
      <b>
        <a href="https://github.com/osisoft/sample-ocs-data_retrieval-power_query_m">Power Query M</a>
      </b>
      <br />
      Shows how to pull data into applications that support Power Query M, such as Power BI and Microsoft Excel.
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-ocs-data_retrieval-power_query_m">Power Query M</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</details>
  
<details><summary><a href="https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/ANALYTICS.md"><b>Analytics</b></a></summary>
<table align="middle" width="100%">
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="docs/DATA_VIEWS.md"> Data Views </a>
      </b>
      <br />
      These samples highlight basic operations of Data Views for Cds, including
      creation, updating, getting data from and deletion of Data Views.
      <a href="docs/DATA_VIEWS.md">Details</a>
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-data_views-java">
              Java
            </a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-data_views-python">
              Python
            </a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-data_views-dotnet">
              .NET
            </a>
          </td>
        </tr>
      </table>
    </td>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-data_views_jupyter-python">Data Views Jupyter</a>
      </b>
      <br />
      This sample demonstrates how to utilize Cds Data Views to do some basic
      data analysis using Python Jupyter Notebook.
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-data_views_jupyter-python">Jupyter Notebook</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-data_views_r-r">Data Views R</a>
      </b>
      <br />
      Demonstrates how to create a data frame in R from an Cds Data View
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-data_views_r-r">R</a>
          </td>
        </tr>
      </table>
    </td>
    <td></td>
  </tr>
</table>
</details>

<details><summary><a href="https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/OTHER.md"><b>Functionality & Utilities</b></a></summary>
<table align="middle" width="100%">
 <tr>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-uom-dotnet">UOM</a>
      </b>
      <br />
      Covers the basic functionality of the UOM system on Cds
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-uom-dotnet">
              .NET
            </a>
          </td>
        </tr>
      </table>
    </td>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-namespace_data_copy-python">Namespace Data Copy</a>
      </b>
      <br />
      Copies Data Views, Assets, and Streams from a source Namespace to a destination Namespace
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-adh-namespace_data_copy-python">
              Python
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="docs/SAMPLE_LIBRARIES.md"> Sample Libraries </a>
      </b>
      <br />
      These sample libraries are used as the base for the other samples. They
      are designed to be straightforward implementations of the REST APIs. They
      are for use in the samples.
      <a href="docs/SAMPLE_LIBRARIES.md"> Details </a>
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a
              href="https://github.com/osisoft/sample-adh-sample_libraries-java"
            >
              Java
            </a>
          </td>
        </tr>
        <tr>
          <td align="middle">
            <a
              href="https://github.com/osisoft/sample-adh-sample_libraries-python"
            >
              Python
            </a>
          </td>
        </tr>
      </table>
    </td>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-ocs-security_management-python">Security Management</a>
      </b>
      <br />
      Covers security configuration within Cds. This includes creating a custom role, creating a user, inviting a user, setting Access Control Lists (ACLs) for collections, setting ACLs for collection items, setting an owner for a collection item, and retrieving access rights.
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a href="https://github.com/osisoft/sample-ocs-security_management-python">
              Python
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-ocs-stream_type_change-python"> Stream Type Change </a>
      </b>
      <br />
      This sample highlights changing an Cds Stream's underlying SDS Type. The main purpose of this sample is to demonstrate the steps necessary to change the underlying SDS Type, and the secondary purpose is to provide an as-is utility to perform this Type change on PI Adapter v1.1 Streams after upgrading to v1.2.
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a
              href="https://github.com/osisoft/sample-ocs-stream_type_change-python"
            >
              Python
            </a>
          </td>
        </tr>
      </table>
    </td>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-pi_to_adh_transfer_verification-powershell"> PI to CONNECT data services Transfer Verification Sample </a>
      </b>
      <br />
      This sample can be used to compare data stored in a PI Data Archive to data written to CONNECT data services through the PI to CONNECT data services agent.
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a
              href="https://github.com/osisoft/sample-adh-pi_to_adh_transfer_verification-powershell"
            >
              PowerShell
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td align="middle" valign="top">
      <b>
        <a href="https://github.com/osisoft/sample-adh-data_hub_to_pi-python"> CONNECT data services to PI </a>
      </b>
      <br />
      This sample uses REST API calls to the Sequential Data Store of CONNECT data services to collect Types, Streams, and data and create corresponding PI Tags in a Data Archive through OMF messages.
      <br />
      <br />
      <table align="middle">
        <tr>
          <td align="middle">
            <a
              href="https://github.com/osisoft/sample-adh-data_hub_to_pi-python"
            >
              Python
            </a>
          </td>
        </tr>
      </table>
    </td>
    <td align="middle" valign="top">
    </td>
  </tr>
</table>
</details>
<br>

**Note**: Tests with automated UI browser components (such as Hybrid Authentication, Authorization Code Flow and Angular samples) fail intermittently due to automation issues.

For OMF to Cds samples please see the OMF repository: [OSI-Samples-OMF](https://github.com/AVEVA/AVEVA-Samples-OMF)

## Credentials

A credential file is used in the samples unless otherwise noted in the sample. The name and location of the credential file should be noted in the sample's ReadMe.  
**Note**: This is not a secure way to store credentials. This is to be used at your own risk.  
You will need to modify these files locally when you run the samples.

## About this repo

The [style guide](https://github.com/osisoft/.github/blob/main/STYLE_GUIDE.md) describes the organization of the repo and the code samples provided. The [test guide](https://github.com/osisoft/.github/blob/main/TEST_GUIDE.md) goes into detail about the included automated tests. The [on prem testing](https://github.com/osisoft/.github/blob/main/ON_PREM_TESTING.md) document describes the software installed on our internal AVEVA build agent.

## Feedback

To request a new sample, if there is a feature or capability you would like demonstrated, or if there is an existing sample you would like in your favorite language, please give us feedback at [https://feedback.aveva.com](https://feedback.aveva.com) under the Developer Samples category. [Feedback](https://datahub.feedback.aveva.com/ideas/search?category=7135134109509567625&query=sample).

## Support

If your support question or issue is related to something with an AVEVA product (an error message, a problem with product configuration, etc...), please open a case with AVEVA Tech Support through myAVEVA Customer Portal ([https://my.osisoft.com](https://my.osisoft.com)).

If your support question or issue is related to a non-modified sample (or test) or documentation for the sample; please email Samples@osisoft.com.

## Contributions

If you wish to contribute please take a look at the [contribution guide](https://github.com/osisoft/.github/blob/main/CONTRIBUTING.md).

## License

[OSI Samples](https://github.com/osisoft/OSI-Samples) are licensed under the [Apache 2 license](LICENSE).
