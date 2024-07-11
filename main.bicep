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
param ContainerAppName string

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

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: 'abbasimart'
}

resource databaseUrlSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'DATABASE-URL'
}

resource testDatabaseUrlSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'TEST-DATABASE-URL'
}

resource secretKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'SECRET-KEY'
}

resource algorithmSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'ALGORITHM'
}

resource cloudinaryCloudSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'CLOUDINARY-CLOUD'
}

resource cloudinaryApiKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'CLOUDINARY-API-KEY'
}

resource cloudinaryApiSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'CLOUDINARY-API-SECRET'
}

resource inventoryTopicSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'INVENTORY-TOPIC'
}

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: ContainerAppName
  location: Location
  properties: {
    managedEnvironmentId: containerEnvironment.id
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
      secrets: [
        {
          name: 'DATABASE_URL'
          value: databaseUrlSecret.properties.value
        }
        {
          name: 'TEST_DATABASE_URL'
          value: testDatabaseUrlSecret.properties.value
        }
        {
          name: 'SECRET_KEY'
          value: secretKeySecret.properties.value
        }
        {
          name: 'ALGORITHM'
          value: algorithmSecret.properties.value
        }
        {
          name: 'CLOUDINARY_CLOUD'
          value: cloudinaryCloudSecret.properties.value
        }
        {
          name: 'CLOUDINARY_API_KEY'
          value: cloudinaryApiKeySecret.properties.value
        }
        {
          name: 'CLOUDINARY_API_SECRET'
          value: cloudinaryApiSecret.properties.value
        }
        {
          name: 'INVENTORY_TOPIC'
          value: inventoryTopicSecret.properties.value
        }
      ]
    }
    template: {
      containers: [
        {
          name: ContainerAppName
          image: Image
          resources: {
            cpu: json('2.0')
            memory: '4Gi'
          }
          env: [
            { name: 'DATABASE_URL', secretRef: 'DATABASE_URL' }
            { name: 'TEST_DATABASE_URL', secretRef: 'TEST_DATABASE_URL' }
            { name: 'SECRET_KEY', secretRef: 'SECRET_KEY' }
            { name: 'ALGORITHM', secretRef: 'ALGORITHM' }
            { name: 'CLOUDINARY_CLOUD', secretRef: 'CLOUDINARY_CLOUD' }
            { name: 'CLOUDINARY_API_KEY', secretRef: 'CLOUDINARY_API_KEY' }
            { name: 'CLOUDINARY_API_SECRET', secretRef: 'CLOUDINARY_API_SECRET' }
            { name: 'INVENTORY_TOPIC', secretRef: 'INVENTORY_TOPIC' }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 4
      }
    }
  }
}
