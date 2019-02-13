/** SdsStream.java
 * 
 *  Copyright 2019 OSIsoft, LLC
 *  
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *  
 *  http://www.apache.org/licenses/LICENSE-2.0>
 *  
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package com.osisoft.ocs_sample_library_preview.sds;

import java.util.List;

public class SdsStream {
    private String Id;
    private String Name;
    private String Description;
    private String TypeId;
    private SdsInterpolationMode InterpolationMode;
    private SdsStreamExtrapolation ExtrapolationMode;
    private List<SdsStreamPropertyOverride> PropertyOverrides;
    private List<SdsTypeProperty> Properties;

    public SdsStream(String name, String typeid) {
        this.Id = name;
        this.Name = name;
        this.TypeId = typeid;
    }

    public SdsStream(String name, String typeid, String description) {
        this.Id = name;
        this.Name = name;
        this.TypeId = typeid;
        this.Description = description;
    }

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        this.Name = name;
    }

    public String getDescription() {
        return Description;
    }

    public void setDescription(String description) {
        this.Description = description;
    }

    public String getTypeId() {
        return TypeId;
    }

    public void setTypeId(String typeId) {
        TypeId = typeId;
    }

    public SdsInterpolationMode getInterpolationMode() {
        return InterpolationMode;
    }

    public void setInterpolationMode(SdsInterpolationMode interpolationMode) {
        InterpolationMode = interpolationMode;
    }

    public SdsStreamExtrapolation getExtrapolationMode() {
        return ExtrapolationMode;
    }

    public void setExtrapolationMode(SdsStreamExtrapolation extrapolationMode) {
        ExtrapolationMode = extrapolationMode;
    }

    public List<SdsStreamPropertyOverride> getPropertyOverrides() {
        return PropertyOverrides;
    }

    public void setPropertyOverrides(List<SdsStreamPropertyOverride> propertyOverrides) {
        this.PropertyOverrides = propertyOverrides;
    }

    public List<SdsTypeProperty> getProperties() {
        return Properties;
    }

    public void setProperties(List<SdsTypeProperty> properties) {
        this.Properties = properties;
    }
}
