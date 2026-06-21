# Golden Worker Examples

Use these as the closest file-shape references when generating worker-related starter code.

## core/worker/SyncWorker.kt

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

## core/worker/SyncScheduler.kt

```kotlin
interface SyncScheduler {
    fun enqueueSync()
}
```

## core/worker/WorkManagerSyncScheduler.kt

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

## core/worker/di/WorkerSchedulerModule.kt

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

## app/App.kt with worker support

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
