Why Qi
======
The Qi Storage Service Business Case
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OSIsoft is known for its time-series data storage engine and its ingress adapters from foreign systems. While the existing software is powerful in many deployment scenarios, the Operations Technology (OT) and Information Technology (IT) convergence is increasingly demanding more flexibility from this same storage pattern in a broader portfolio of industries.

The advent of Platform as a Service computing at scale and "information economy" practices have created compelling scenarios that fundamentally change deployment, redundancy, and fault tolerance demands on software infrastructure. OSIsoft firmly believes that industrial grade infrastructure and cross-discipline creativity requirements cannot be matched by virtualizing existing software.

What remains unique amongst these requirements is a flexible, ordered, highly scalable, distributed storage pattern. OSIsoft sees this as a new path forward - a fundamentally transformational opportunity to offer this highly available, hybrid-deployment capable, and imminently repurposeable storage infrastructure as a service. 

This service is intended to be consumed and packaged into platforms for use by OSIsoft, partners, and other OEMs or developers, to create or enhance new markets and products that will benefit almost any type of user.

Infrastructure to Platform
^^^^^^^^^^^^^^^^^^^^^^^^^^
The infrastructure-level storage pattern and technology stack known as "Qi" is designed to enable a new class of platform-oriented, software as a service offerings created by OSIsoft, its partners, and third party developers.

When consumed as a service by users, it can be colloquially referred to as a "Distributed Historian as a Service"; however this is only one dimension of its capability. The fundamental Qi storage service technology can be repackaged in several ways.

1.1.1. Enterprise Packaging
^^^^^^^^^^^^^^^^^^^^^^^^^^^
OSIsoft's customer base will not be exposed to the Qi storage service directly. Existing and new markets will be offered a set of compelling, modern services around Qi's technology to create a familiar "distributed historian as a service" offering.

Additionally, the Qi storage service will be reused as the basis of two classes of products:
*	Entirely new SaaS offerings
*	Transition from / Extensions of legacy products

These will be designed as horizontal scenarios that enable customers to take advantage of other storage and analytical services available in Microsoft Azure.

1.1.2. Partner / OEM Packaging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Partners and OEMs will have access to Qi storage service (or one of the aforementioned wrappings of it) as a finished product via appropriate Web-enabled technologies (e.g. REST, Web Sockets, or AMQP) to store and access data for use in their applications. A "functional language exposure" would extend the higher level operations available on data stored within Qi.

To develop a rich partner OSIsoft and Microsoft partner ecosystem, a first-class scenario will support the application of partner licensed algorithms to data within a Qi storage instance to enable rich data post-processing. These advanced "Marketplace Scenarios" are yet to be detailed. Cross-cloud provider scenarios are also not out of the question, but not yet required by customer demand.

Billing and accounting will be a function of use metrics. It is expected that Microsoft Azure's commerce features could perform revenue sharing with OSIsoft (and others) for use given proper accounting and use metrics.

Through the use of Microsoft Azure's "Mobile Services", it may be possible to wrap either a platform or infrastructure level experience for a third party so a feature set could be "white-labeled" yet still consistently maintained by OSIsoft.

It is envisioned that some partners would choose to enhance existing service offerings by creating an "Enhanced" or "High Fidelity" version of their platform (e.g. if a similar storage pattern exists on regular Blob storage, offer a "Qi-based" up-sale version), or build entirely new SaaS offerings for sale.

1.1.3. Developer Packaging
^^^^^^^^^^^^^^^^^^^^^^^^^^
A developer should be able to consume the Qi storage service in an appropriate manner and be charged via Microsoft's Azure commerce methods and share revenue with OSIsoft.

It is envisioned that some partners and end-users / customers of OSIsoft would engage with this pattern to do custom development (e.g. large IT shops may consume both a packaged version and development version for internal purposes).

It would be required that any third-party development deployment resource remain "in-step" version-wise with the main version of both Microsoft Azure and OSIsoft's infrastructure technologies.

1.2. Flexible Deployment, Data Types, and Emerging Patterns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Two major features that differentiate OSIsoft's use cases from existing "Internet of Things" narratives are deployment practices and persisting native machine data types in their original structure and format. 

Combining these differentiators with emerging use patterns in a hybrid-deployment-capable Platform as a Service infrastructure will open a range of new opportunities for a broad set of customers.

1.2.1. Deployment
^^^^^^^^^^^^^^^^^
While existing OSIsoft customers are swaddled in several layers of firewalls and routers, this may change drastically in the near future.

The reality of their deployment is somewhat driven by "security requirements", however, in many cases the "disconnected operations" reality for these customers becomes far more important. Many customers must be able to work in a "frequently disconnected" (intentional) or disaster-recovery (unintentional) state.

In order to enable this, the Qi storage pattern requires two main features:

*	Buffering / spooling data during disconnected states
*	Local data access in case of disaster or localized network trauma
*	Zero configuration / deployment / maintenance of the services themselves

Microsoft Azure has some planned features that would assist in implementation of these scenarios, and the Qi storage pattern incorporates specific engineering to enable these patterns.

1.2.2. Dynamic Data Types
^^^^^^^^^^^^^^^^^^^^^^^^^
While it may intuitively appear that machines generate consistent data over time, in practice, this is not true.

In many cases the metadata, schema, or actual deterioration of sensors will affect the data payload that is sensed and reported to the system of record. The resulting data quality requires "quality indicators" to assist in its consumption.

As sensors evolve and change at customer sites, OSIsoft recognizes that machines will increase their sensing capabilities. Existing customers may deploy a greater quantity, or "smarter" sensors, and / or sometimes they will take advantage of new sensing patterns that move, change orientation, or even change data types dynamically. The result is that devices or systems make unexpected changes to their data schema (through unintended, or intended intervention).

The transmission and storage pattern will not attempt to enforce consistency in the face of exogenous changes. Rather, these changes must be recorded and variations in data quality, auditing, and faults must be noted or flagged.

1.2.3. Emerging Patterns
^^^^^^^^^^^^^^^^^^^^^^^^
The Qi storage pattern - whether used as a product (e.g. "a distributed historian as a service") or as a resource in an embedded service is designed to deliver on the promise of the Platform as a Service flexibility for the imaginative developer. The rapid delivery pattern used by OSIsoft's services team will insure that the Qi service and storage pattern will enhance its peer storage and analytical patterns within Microsoft Azure.

1.3. Natural Fidelity, Flexible Indices, Deep History
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
OSIsoft was built on the understanding that data comes in several shapes, relationships, and frequencies. Patterns eventually emerge as data volumes and velocities grow. 

Keeping these fundamental building blocks available to consumers and applications for extended ranges will continue to deliver value as new patterns are enabled through service-based computing.

1.3.1. Natural Fidelity from Data Sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Simply put - recording data as it is produced is contingent upon several factors prior to its ultimate delivery to durable storage. Using optimized techniques over the wire and disk, OSIsoft is able to record data that is appropriate to the measurement device's specifications (within its tolerances). This is accomplished while also efficiently delivering the data required for creating rich, immersive user experiences within applications and devices.

Due to the fact that sensors emit signals or data via various methods, sampling techniques that may be relevant to other disciplines are not conducive to the capture and preservation of the raw data at its "natural fidelity".

In turn, the projection of the raw data for use in other disciplines requires infrastructure-level support. This feature provides appropriate calculations that result in meaningful, contextual, data extractions prior to their delivery to upstream analytical engines.

By including native ingress and egress methods in the Qi storage service, developers, Partners, OEMs, and OSIsoft will deliver flexible, first-class signal-to-data and data-to-information experiences efficiently to any consumer.

1.3.2. Flexible Indices
^^^^^^^^^^^^^^^^^^^^^^^
When storing large volumes of data, OSIsoft traditionally defaulted to the "time-series" domain as its primary index. 

However, in today's world, the data context is as important as its timestamp. To account for this, the Qi storage pattern must be capable of selecting a dominant index as well as support for ancillary indexing mechanisms.

Therefore Qi's native range query support relies on a dominant index, but its fundamental data schemas allow applications to build more flexible means of identifying patterns of interest directly from the data being recorded.

This feature set allows for Qi to be deeply integrated with ancillary Windows Azure infrastructure services and extensible data type storage within Qi itself.

1.3.3. Deep History on Tap
^^^^^^^^^^^^^^^^^^^^^^^^^^
Pattern recognition, autocorrelation, partial autocorrelation, and seasonality are difficult (or misleading) when applied to small amounts of data. That's why the core competency of Qi is keeping large volumes of ordered data streams on-tap for rapid replay and analysis.

Whether users require real-time situational awareness or deep historical analytics, the Qi storage service will deliver the right range of data to the consumer.

1.4. Distributed, Fault Tolerant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Building an infrastructure that enables moving existing customers off-premises and takes advantage of scale-out, serving multiple regions, and fault tolerance across regions.

1.4.1. Distributed Systems
^^^^^^^^^^^^^^^^^^^^^^^^^^
The Qi storage service supports the natural growth patterns of consumers. Whether the destination of that data is a shared information production workflow, or secure delivery to joint-venture target audiences - the service itself must natively support tomorrow's connected operations.

These patterns must respect logical, geographic, and security / privacy boundaries while still maintaining trustworthiness of its underlying service provider. To enable this, Qi will take advantage of Microsoft Azure's capability to target data to particular data centers across regions to respect customer interests.

1.4.2. Fault Tolerant in the Face of Adversity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In OSIsoft's world, potential data loss and / or downtime can arise from a number of sources. Years of experience have led to a design that allows for both disconnected operation scenarios as well as optimized re-connection patterns. 

The Qi storage service will leverage Microsoft Azure's core features to insure replication and redundancy as well as service availability. Features within the data delivery mechanisms in Qi will reduce the opportunity for data loss. Additional work has been done to deliver best-case scenario disconnected operations for consumers that experience "deep isolation" and disconnection events where cloud services become unavailable for extended periods of time.

1.5. Deep Integration
^^^^^^^^^^^^^^^^^^^^^
As a standalone resource, the Qi storage service offers a compelling distributed "raw historian" type of infrastructure for high fidelity, ordered data with varied schemas. 

OSIsoft's Qi-based offerings (and Qi itself) have been designed to delight both developers and consumers alike by producing experiences that effortlessly incorporate domain expertise naturally into the solutions they envision. 

As an enhancement to Microsoft Azure, new experiences to existing and planned services can incorporate this rich set of domain expertise to satisfy even the most demanding user-centered activities.

Some examples include: 

1.5.1. Machine Learning / Passau / CloudML
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Building a native "module" (or set of modules) in Passau will allow users to perform cleansing operations, feed data into Passau, and build models that help operationalize machine learning directly from well-groomed, shaped, and projected data that is persisted in the Qi storage service.

The flexible schemas within Qi mean that well-ordered results from Passau could be returned to Qi to enrich any operations scenario. This enables a virtuous cycle between Operations Technology and data scientists.


1.5.2. Reykjavik / ISS Enhancements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The native data recorded in the Qi storage service and the Internet of Things (IoT) space targeted by Reykjavik and Intelligent Systems Services (ISS) are related, but not entirely overlapping.

The Qi storage service is a direct fit to leverage and enhance Reykjavik's telemetry / filtering (following the Kafka design pattern). Additionally, Qi can enhance ISS by providing certain customers deeper reach into their data for longer term historical analysis (or higher fidelity) device data (e.g. "ISS HD").

Microsoft's intended partners and OEMs in the Reykjavik and ISS space (OSIsoft included) could all draw benefit from leveraging the Qi storage technology in concert with the rest of Microsoft Azure.


1.5.3. Power BI / HDInsight / Analytics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By providing integration to and from other analytical services that can leverage the Qi storage service would provide a mechanism for users to naturally leverage the "correct storage" for their needs. This is the goal, in essence, of any deep integration within Microsoft Azure.

Seamlessly allowing users to express their question appropriately and project data from several storage patterns, align it, and then visualize their results is the goal of integrating Qi into this technology set.

1.6. Conclusion
^^^^^^^^^^^^^^^
OSIsoft is crafting the Qi storage service and technology stack to deliver its industry-leading domain expertise to existing and new audiences. Its implementation on Microsoft Azure and purposeful generalization will enable scenarios that help today's customers and empower new business opportunities.

OSIsoft sees its path forward in a distributed world leveraging the strengths of its partner community and offering its customers a coherent, seamless way to deliver streaming "data coverage" to information workers, partners, and developers in an engaging, flexible way that rewards their curiosity




``Confidential | OSIsoft, LLC | © 2014
via OSIsoft Research & The Ministry of Innovation``
