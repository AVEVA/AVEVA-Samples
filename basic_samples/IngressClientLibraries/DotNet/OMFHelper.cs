// <copyright file="OMFHelper.cs" company="OSIsoft, LLC">
//
//Copyright 2019 OSIsoft, LLC
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//<http://www.apache.org/licenses/LICENSE-2.0>
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.
// </copyright>

using OSIsoft.Models.OMF;
using System;
using System.Collections.Generic;
using System.Text;

namespace IngressClientLibraries
{
    class OMFHelper
    {
        public static OMFMessage GenerateOMFTypeMessage(string messageBody, MessageAction action)
        {
            OMFMessage omfType = new OMFMessage()
            {
                MessageType = MessageType.Type,
                Action = action,
                MessageFormat = MessageFormat.JSON,
                Body = Encoding.UTF8.GetBytes(messageBody),
                Version = OMFConstants.DefaultOMFVersion
            };
            return omfType;
        }

        public static OMFMessage GenerateOMFContainerMessage(string messageBody, MessageAction action)
        {
            OMFMessage omfContainer = new OMFMessage()
            {
                MessageType = MessageType.Container,
                Action = action,
                MessageFormat = MessageFormat.JSON,
                Body = Encoding.UTF8.GetBytes(messageBody),
                Version = OMFConstants.DefaultOMFVersion
            };
            return omfContainer;
        }

        public static OMFMessage GenerateOMFDataMessage(string messageBody, MessageAction action)
        {
            OMFMessage omfDataMessage = new OMFMessage()
            {
                MessageType = MessageType.Data,
                Action = action,
                MessageFormat = MessageFormat.JSON,
                Body = Encoding.UTF8.GetBytes(messageBody),
                Version = OMFConstants.DefaultOMFVersion
            };
            return omfDataMessage;
        }
    }
}
