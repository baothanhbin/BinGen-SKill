# Core Module Patterns

Use this file when generating or refining `core/*` modules.

## Module Intent

- `core:model`: small shared models and enums
- `core:theme`: Material theme, colors, typography
- `core:ui`: tiny shared UI helpers only
- `core:network`: Ktor clients, network datasource, DI
- `core:data`: repository contracts, implementations, bindings
- `core:database`: Room entities, DAO, database, DI
- `core:datastore`: Proto definitions, serializers, local persistence
- `core:worker`: WorkManager workers and scheduler abstractions for default background tasks

## resources

Use `:resources` for:
- shared strings used by `app`
- bottom bar and top-level destination labels
- starter feature copy that would otherwise be duplicated or hardcoded

Default rule:
- if text is shown in UI and is not ephemeral debug text, put it in `resources/src/main/res/values/strings.xml`
- use `stringResource(...)` in Compose
- when app shell models need labels, prefer `@StringRes` ids over raw `String`

## Plugin Rule

Only Compose-facing modules should use the compose module convention:
- `core:theme`
- `core:ui`

Non-UI modules should use the plain android module convention:
- `core:model`
- `core:network`
- `core:data`
- `core:database`
- `core:datastore`
- `core:worker`

## core:network

Expected files:

```text
core/network/
  build.gradle.kts
  src/main/java/<base-package>/core/network/
    NetworkModule.kt
    NetworkClients.kt
    NetworkDataSource.kt
```

Pattern:

```kotlin
object NetworkModule {
    private const val API_BASE_URL = BuildConfig.API_BASE_URL

    fun provideClient(baseUrl: String): HttpClient {
        return HttpClient(OkHttp) {
            defaultRequest {
                url(baseUrl)
            }
            install(ContentNegotiation) {
                json(Json {
                    ignoreUnknownKeys = true
                    encodeDefaults = true
                })
            }
        }
    }

    fun provideAuthHttpClient(): HttpClient {
        return provideClient("$API_BASE_URL/api/auth/")
    }
}

object NetworkClients {
    private const val API_BASE_URL = BuildConfig.API_BASE_URL

    val authClient: HttpClient = NetworkModule.provideAuthHttpClient()
    val historyClient: HttpClient = NetworkModule.provideClient("$API_BASE_URL/api/history/")
}

class NetworkDataSource @Inject constructor(
)
{
    suspend fun login(request: LoginRequest): AuthResponse {
        return NetworkClients.authClient.post("login") {
            contentType(ContentType.Application.Json)
            setBody(request)
        }.body()
    }
}
```

Default fresh-project rule:
- keep endpoint-group clients in `NetworkClients.kt`
- include one extra example client such as `historyClient` so the extension pattern is obvious
- let `NetworkDataSource.kt` call `NetworkClients.xxxxx`
- let repositories call the datasource instead of posting directly from feature code

## core:data

Expected files:

```text
core/data/
  repository/
    AuthRepository.kt
  impl/
    AuthRepositoryImpl.kt
  di/
    DataModule.kt
```

Pattern:

```kotlin
interface AuthRepository {
    val isLoggedIn: Flow<Boolean>
    suspend fun login(request: LoginRequest): Result<AuthResponse>
    suspend fun getToken(): String?
}

class AuthRepositoryImpl @Inject constructor(
    private val authDataStore: AuthDataStore,
    private val networkDataSource: NetworkDataSource,
) : AuthRepository {
    override val isLoggedIn: Flow<Boolean> = authDataStore.isLoggedInFlow()

    override suspend fun login(request: LoginRequest): Result<AuthResponse> {
        return runCatching {
            networkDataSource.login(request)
        }.onSuccess { response ->
            response.token.takeIf { it.isNotBlank() }?.let { token ->
                authDataStore.saveSession(token, response.userId)
            }
        }
    }

    override suspend fun getToken(): String? = authDataStore.getToken()
}
```

Use `@Binds` for interface-to-implementation mapping when possible.

## core:database

Expected files:

```text
core/database/
  AppDatabase.kt
  dao/
    PlaceholderDao.kt
  model/
    PlaceholderEntity.kt
  di/
    DatabaseModule.kt
```

Rules:
- use the neutral name `AppDatabase`
- keep entities/dao/di in separate files
- expose at least one DAO from the database
- provide the database with Hilt

## core:datastore

Expected files:

```text
core/datastore/
  src/main/proto/auth.proto
  src/main/java/<base-package>/core/datastore/
    AuthDataStore.kt
```

Rules:
- keep `.proto` under `src/main/proto`
- expose a thin local data source API
- handle IO errors with `catch`
- keep serializer details close to the data store implementation unless there is enough complexity to split it out

## core:theme

The starter theme should be small but production-shaped:
- include `Color.kt` for reusable palette tokens
- include `Font.kt` for starter font families or safe fallbacks
- include `Type.kt` for `Typography`
- include one theme entrypoint such as `AppTheme` in `Theme.kt`
- stay Material3 based
- avoid random duplicate theme files

## core:ui

Only add reusable items that are cross-feature:
- tiny state holders
- reusable dialogs
- shared components
- shared navigation transitions
- shared loading/feedback overlays

Do not move feature-specific components into `core:ui`.

Expected starter files:

```text
core/ui/
  feedback/
    LoadingOverlay.kt
  navigation/
    ScreenTransitions.kt
  util/
    LocationStateHolder.kt
```

## core:worker

Expected files:

```text
core/worker/
  build.gradle.kts
  src/main/java/<base-package>/core/worker/
    SyncWorker.kt
    SyncScheduler.kt
    WorkManagerSyncScheduler.kt
    di/
      WorkerSchedulerModule.kt
```

Rules:
- workers should not depend on `feature/*`
- workers should inject repository or coordinator services from `core:data`
- app-level WorkManager setup belongs in `app/App.kt`
- use `@HiltWorker` + `@AssistedInject` for workers

Pattern:

```kotlin
@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted params: WorkerParameters,
    private val authRepository: AuthRepository,
) : CoroutineWorker(appContext, params) {

    override suspend fun doWork(): Result {
        val token = authRepository.getToken() ?: return Result.retry()
        return Result.success()
    }
}
```
