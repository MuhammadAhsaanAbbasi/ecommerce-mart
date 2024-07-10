@description('Application Suffix that will be used & applied on some resources')
param AppSuffix string = uniqueString(resourceGroup().id)

@description('The location to deploy all resources')
param Location string = resourceGroup().location

@description('The name of the log Analytics Workspace')
param logAnalyticsWorkspaceName string = 'log-analytics-${AppSuffix}'

@description('The name of the Application Insights Workspace')
param appInsightsWorkspaceName string = 'app-insights-${AppSuffix}'

@description('The name of the Container App Environment')
param containerAppEnvironmentName string = 'container-app-environment-${AppSuffix}'

@description('The Docker Imaage name to deploy on Container')
param Image string

@description('The name of the Container App')
param containerAppName string

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsWorkspaceName
  location: Location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource appInsightsWorkspace 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsWorkspaceName
  location: Location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

resource containerEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: containerAppEnvironmentName
  location: Location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listkeys().primarySharedKey
      }
    }
  }
}

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: containerAppName
  location: Location
  properties: {
    managedEnvironmentId:containerEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        allowInsecure: false
        traffic: [
          {
            latestRevision: true
            weight: 100
          }
        ]
      }
    }
    template: {
      containers: [
        {
          name: containerAppName
          image: Image
          resources: {
            cpu: json('2.0')
            memory: '4Gi'
          }
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 5
      }
    }
  }
}
