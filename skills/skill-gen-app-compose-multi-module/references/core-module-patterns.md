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
- `core:alarm`: scheduler or receiver shell
- `core:worker`: WorkManager workers and scheduler abstractions

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
- `core:alarm`
- `core:worker`

## core:network

Expected files:

```text
core/network/
  build.gradle.kts
  src/main/java/<base-package>/core/network/
    NetworkModule.kt
    NetworkDataSource.kt
```

Pattern:

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideAuthHttpClient(): HttpClient {
        return HttpClient(OkHttp) {
            defaultRequest {
                url(BuildConfig.API_BASE_URL)
            }
            install(ContentNegotiation) {
                json(Json { ignoreUnknownKeys = true })
            }
        }
    }
}

class NetworkDataSource @Inject constructor(
    private val authClient: HttpClient,
)
```

Do not leave network access as a bare global object if Hilt wiring is already part of the architecture.

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
    suspend fun getToken(): String?
}

class AuthRepositoryImpl @Inject constructor(
    private val authDataStore: AuthDataStore,
) : AuthRepository {
    override val isLoggedIn: Flow<Boolean> = authDataStore.isLoggedInFlow()

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

The starter theme can stay small, but must be coherent:
- one theme entrypoint such as `AppTheme`
- Material3 based
- no random duplicate theme files

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
