# Worker Patterns

Use this file when the new project needs WorkManager, sync jobs, retries, periodic jobs, or background processing.

## Module Placement

Default to `core:worker` for background jobs.

Why:
- workers are infra, not feature UI
- multiple features can depend on one background scheduler
- workers should consume repository/coordinator abstractions from `core:data`

## Worker DI Rules

- annotate workers with `@HiltWorker`
- use `@AssistedInject`
- use `@Assisted` for `Context` and `WorkerParameters`
- inject repositories or coordinator services, not composables or ViewModels

Example:

```kotlin
@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted params: WorkerParameters,
    private val authRepository: AuthRepository,
) : CoroutineWorker(appContext, params) {

    override suspend fun doWork(): Result {
        val token = authRepository.getToken() ?: return Result.retry()

        return runCatching {
            // real sync goes here
        }.fold(
            onSuccess = { Result.success() },
            onFailure = { Result.retry() },
        )
    }
}
```

## Scheduler Abstraction

Expose an interface for enqueueing work:

```kotlin
interface SyncScheduler {
    fun enqueueSync()
}
```

Concrete implementation:

```kotlin
class WorkManagerSyncScheduler @Inject constructor(
    @ApplicationContext private val context: Context,
) : SyncScheduler {

    override fun enqueueSync() {
        val request = OneTimeWorkRequestBuilder<SyncWorker>().build()
        WorkManager.getInstance(context).enqueue(request)
    }
}
```

Bind it with Hilt:

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class WorkerSchedulerModule {

    @Binds
    abstract fun bindSyncScheduler(
        impl: WorkManagerSyncScheduler,
    ): SyncScheduler
}
```

## App Wiring

If the project has workers, `App.kt` should provide `HiltWorkerFactory`:

```kotlin
@HiltAndroidApp
class App : Application(), Configuration.Provider {

    @Inject
    lateinit var workerFactory: HiltWorkerFactory

    override val workManagerConfiguration: Configuration
        get() = Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()
}
```

## Dependencies

Expect these dependencies in worker-ready projects:
- `androidx.work:work-runtime-ktx`
- `androidx.hilt:hilt-work`
- the Hilt compiler path already used by the repo

## Do Not Do

- do not inject `ViewModel` into workers
- do not place workers under `feature/*`
- do not let workers call UI-only classes
- do not skip `HiltWorkerFactory` wiring if using Hilt workers
