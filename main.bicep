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

@description('The Docker Image name to deploy on Container')
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
  name: 'database-urls'
}

resource testDatabaseUrlSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'tests-database-url'
}

resource secretKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'secret-keys'
}

resource algorithmSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'algorithim'
}

resource cloudinaryCloudSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'cloudinary-clouds'
}

resource cloudinaryApiKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'cloudinary-api-keys'
}

resource cloudinaryApiSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'cloudinary-api-secrets'
}

resource inventoryTopicSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' existing = {
  parent: keyVault
  name: 'inventory-topics'
}

// resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-07-31-preview' existing = {
//   name: 'hrk-ecommerce-mart'
//   scope: resourceGroup()
// }

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
          name: 'database-urls'
          keyVaultUrl: databaseUrlSecret.properties.secretUriWithVersion
          identity: 'system'
        }
        {
          name: 'tests-database-url'
          keyVaultUrl: testDatabaseUrlSecret.properties.secretUriWithVersion
          identity: 'system'
        }
        {
          name: 'secret-keys'
          keyVaultUrl: secretKeySecret.properties.secretUriWithVersion
          identity: 'system'
        }
        {
          name: 'algorithim'
          keyVaultUrl: algorithmSecret.properties.secretUriWithVersion
          identity: 'system'
        }
        {
          name: 'cloudinary-clouds'
          keyVaultUrl: cloudinaryCloudSecret.properties.secretUriWithVersion
          identity: 'system'
        }
        {
          name: 'cloudinary-api-keys'
          keyVaultUrl: cloudinaryApiKeySecret.properties.secretUriWithVersion
          identity: 'system'
        }
        {
          name: 'cloudinary-api-secrets'
          keyVaultUrl: cloudinaryApiSecret.properties.secretUriWithVersion
          identity: 'system'
        }
        {
          name: 'inventory-topics'
          keyVaultUrl: inventoryTopicSecret.properties.secretUriWithVersion
          identity: 'system'
        }
      ]
      activeRevisionsMode: 'Multiple'
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
            { name: 'DATABASE_URL', secretRef: 'database-urls' }
            { name: 'TEST_DATABASE_URL', secretRef: 'tests-database-url' }
            { name: 'SECRET_KEY', secretRef: 'secret-keys' }
            { name: 'ALGORITHM', secretRef: 'algorithim' }
            { name: 'CLOUDINARY_CLOUD', secretRef: 'cloudinary-clouds' }
            { name: 'CLOUDINARY_API_KEY', secretRef: 'cloudinary-api-keys' }
            { name: 'CLOUDINARY_API_SECRET', secretRef: 'cloudinary-api-secrets' }
            { name: 'INVENTORY_TOPIC', secretRef: 'inventory-topics' }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 3
        rules: [
          {
            name: 'http-rule'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
        ]
      }
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}
