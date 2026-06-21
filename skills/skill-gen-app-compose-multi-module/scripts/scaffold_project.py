#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from textwrap import dedent


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "app"


def package_to_path(package_name: str) -> Path:
    return Path(*package_name.split("."))


def catalog_accessor(alias: str) -> str:
    return alias.replace("-", ".")


def plugin_ref(alias: str) -> str:
    return f"libs.plugins.{catalog_accessor(alias)}"


def library_ref(alias: str) -> str:
    return f"libs.{catalog_accessor(alias)}"


def feature_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[^a-zA-Z0-9]+", name) if part)


def feature_camel(name: str) -> str:
    pascal = feature_pascal(name)
    return pascal[:1].lower() + pascal[1:] if pascal else name


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def touch_text_file(path: Path, content: str = "") -> None:
    write_file(path, content)


def module_build_common(namespace: str, plugin_alias: str) -> str:
    return dedent(
        f"""
        plugins {{
            alias({plugin_ref(plugin_alias)})
        }}

        android {{
            namespace = "{namespace}"
        }}
        """
    ).strip()


def create_root_files(root: Path, project_name: str, slug: str, module_includes: list[str]) -> None:
    includes = "\n".join(f'include("{item}")' for item in module_includes)
    write_file(
        root / "settings.gradle.kts",
        dedent(
            f"""
            pluginManagement {{
                repositories {{
                    google {{
                        content {{
                            includeGroupByRegex("com\\\\.android.*")
                            includeGroupByRegex("com\\\\.google.*")
                            includeGroupByRegex("androidx.*")
                        }}
                    }}
                    mavenCentral()
                    gradlePluginPortal()
                }}
            }}
            dependencyResolutionManagement {{
                repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
                repositories {{
                    google()
                    mavenCentral()
                }}
            }}

            enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")

            rootProject.name = "{project_name}"
            includeBuild("build-logic")
            {includes}
            """
        ),
    )

    write_file(
        root / "build.gradle.kts",
        dedent(
            """
            plugins {
                alias(libs.plugins.android.application) apply false
                alias(libs.plugins.jetbrains.kotlin.android) apply false
                alias(libs.plugins.jetbrains.kotlin.plugin.compose) apply false
                alias(libs.plugins.jetbrains.kotlin.jvm) apply false
                alias(libs.plugins.google.devtools.ksp) apply false
                alias(libs.plugins.android.library) apply false
                alias(libs.plugins.jetbrains.kotlin.plugin.serialization) apply false
                alias(libs.plugins.google.dagger.hilt.android) apply false
                alias(libs.plugins.androidx.room) apply false
                alias(libs.plugins.google.protobuf) apply false
            }
            """
        ),
    )

    write_file(
        root / "gradle.properties",
        dedent(
            """
            org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
            android.useAndroidX=true
            kotlin.code.style=official
            android.nonTransitiveRClass=true
            api.baseUrl=https://api.example.com
            """
        ),
    )

    write_file(
        root / "gradle" / "libs.versions.toml",
        dedent(
            f"""
            [versions]
            agp = "8.13.0"
            kotlin = "2.0.21"
            coreKtx = "1.16.0"
            hilt = "2.52"
            navigationCompose = "2.9.4"
            lifecycleRuntimeKtx = "2.9.4"
            hiltNavigationCompose = "1.3.0"
            activityCompose = "1.10.0"
            composeBom = "2025.09.01"
            appcompat = "1.7.1"
            room = "2.8.1"
            protobuf = "4.28.2"
            googleProtobuf = "0.9.5"
            kotlinxSerialization = "1.7.3"
            ktorSerializationKotlinxJson = "2.3.12"
            datastore = "1.1.7"
            material3 = "1.4.0"
            material = "1.13.0"
            junit = "4.13.2"
            junitVersion = "1.3.0"
            espressoCore = "3.7.0"
            jetbrainsKotlinJvm = "2.0.21"
            kotlinComposeCompiler = "2.0.21"
            ksp = "2.0.21-1.0.25"

            [libraries]
            androidx-core-ktx = {{ group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }}
            androidx-lifecycle-runtime-ktx = {{ group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycleRuntimeKtx" }}
            androidx-activity-compose = {{ group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }}
            androidx-compose-bom = {{ group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }}
            androidx-ui = {{ group = "androidx.compose.ui", name = "ui" }}
            androidx-ui-graphics = {{ group = "androidx.compose.ui", name = "ui-graphics" }}
            androidx-ui-tooling = {{ group = "androidx.compose.ui", name = "ui-tooling" }}
            androidx-ui-tooling-preview = {{ group = "androidx.compose.ui", name = "ui-tooling-preview" }}
            androidx-ui-test-manifest = {{ group = "androidx.compose.ui", name = "ui-test-manifest" }}
            androidx-ui-test-junit4 = {{ group = "androidx.compose.ui", name = "ui-test-junit4" }}
            androidx-material3 = {{ group = "androidx.compose.material3", name = "material3", version.ref = "material3" }}
            androidx-appcompat = {{ group = "androidx.appcompat", name = "appcompat", version.ref = "appcompat" }}
            material = {{ group = "com.google.android.material", name = "material", version.ref = "material" }}
            hilt-android = {{ group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }}
            dagger-hilt-complier = {{ group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }}
            androidx-hilt-navigation-compose = {{ group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "hiltNavigationCompose" }}
            androidx-hilt-complier = {{ group = "androidx.hilt", name = "hilt-compiler", version.ref = "hiltNavigationCompose" }}
            androidx-navigation-compose = {{ module = "androidx.navigation:navigation-compose", version.ref = "navigationCompose" }}
            androidx-room-compiler = {{ module = "androidx.room:room-compiler", version.ref = "room" }}
            androidx-room-ktx = {{ module = "androidx.room:room-ktx", version.ref = "room" }}
            androidx-room-runtime = {{ module = "androidx.room:room-runtime", version.ref = "room" }}
            androidx-datastore = {{ group = "androidx.datastore", name = "datastore", version.ref = "datastore" }}
            protobuf-kotlin-lite = {{ group = "com.google.protobuf", name = "protobuf-kotlin-lite", version.ref = "protobuf" }}
            protobuf-protoc = {{ group = "com.google.protobuf", name = "protoc", version.ref = "protobuf" }}
            kotlinx-serialization-json = {{ group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinxSerialization" }}
            ktor-serialization-kotlinx-json = {{ module = "io.ktor:ktor-serialization-kotlinx-json", version.ref = "ktorSerializationKotlinxJson" }}
            junit = {{ group = "junit", name = "junit", version.ref = "junit" }}
            androidx-junit = {{ group = "androidx.test.ext", name = "junit", version.ref = "junitVersion" }}
            androidx-espresso-core = {{ group = "androidx.test.espresso", name = "espresso-core", version.ref = "espressoCore" }}
            android-gradlePlugin = {{ group = "com.android.tools.build", name = "gradle", version = "8.12.3" }}
            ksp-gradlePlugin = {{ group = "com.google.devtools.ksp", name = "com.google.devtools.ksp.gradle.plugin", version.ref = "ksp" }}
            room-gradlePlugin = {{ group = "androidx.room", name = "room-gradle-plugin", version.ref = "room" }}
            kotlin-gradlePlugin = {{ group = "org.jetbrains.kotlin", name = "kotlin-gradle-plugin", version.ref = "kotlin" }}

            [plugins]
            android-application = {{ id = "com.android.application", version.ref = "agp" }}
            android-library = {{ id = "com.android.library", version.ref = "agp" }}
            jetbrains-kotlin-android = {{ id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }}
            jetbrains-kotlin-jvm = {{ id = "org.jetbrains.kotlin.jvm", version.ref = "jetbrainsKotlinJvm" }}
            jetbrains-kotlin-plugin-serialization = {{ id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }}
            jetbrains-kotlin-plugin-compose = {{ id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlinComposeCompiler" }}
            google-dagger-hilt-android = {{ id = "com.google.dagger.hilt.android", version.ref = "hilt" }}
            google-devtools-ksp = {{ id = "com.google.devtools.ksp", version.ref = "ksp" }}
            androidx-room = {{ id = "androidx.room", version.ref = "room" }}
            google-protobuf = {{ id = "com.google.protobuf", version.ref = "googleProtobuf" }}

            {slug}-compose-application = {{ id = "{slug}.compose.application", version = "unspecified" }}
            {slug}-compose-module = {{ id = "{slug}.compose.module", version = "unspecified" }}
            {slug}-feature = {{ id = "{slug}.feature", version = "unspecified" }}
            {slug}-room = {{ id = "{slug}.room", version = "unspecified" }}
            {slug}-module = {{ id = "{slug}.module", version = "unspecified" }}
            {slug}-hilt = {{ id = "{slug}.hilt", version = "unspecified" }}
            """
        ),
    )

    write_file(
        root / "build-logic" / "settings.gradle.kts",
        dedent(
            """
            dependencyResolutionManagement {
                repositories {
                    google()
                    mavenCentral()
                }
                versionCatalogs {
                    create("libs") {
                        from(files("../gradle/libs.versions.toml"))
                    }
                }
            }

            rootProject.name = "build-logic"
            include(":convention")
            """
        ),
    )

    write_file(
        root / "build-logic" / "convention" / "build.gradle.kts",
        dedent(
            f"""
            import org.jetbrains.kotlin.gradle.dsl.JvmTarget

            plugins {{
                `kotlin-dsl`
            }}

            java {{
                sourceCompatibility = JavaVersion.VERSION_17
                targetCompatibility = JavaVersion.VERSION_17
            }}

            kotlin {{
                compilerOptions {{
                    jvmTarget = JvmTarget.JVM_17
                }}
            }}

            dependencies {{
                compileOnly(libs.android.gradlePlugin)
                compileOnly(libs.ksp.gradlePlugin)
                compileOnly(libs.room.gradlePlugin)
                compileOnly(libs.kotlin.gradlePlugin)
                compileOnly("androidx.room:room-gradle-plugin:2.8.2")
            }}

            gradlePlugin {{
                plugins {{
                    register("androidComposeApplication") {{
                        id = "{slug}.compose.application"
                        implementationClass = "AndroidApplicationComposePlugin"
                    }}
                    register("androidComposeLibrary") {{
                        id = "{slug}.compose.module"
                        implementationClass = "AndroidLibraryComposePlugin"
                    }}
                    register("featureConvention") {{
                        id = "{slug}.feature"
                        implementationClass = "AndroidFeaturePlugin"
                    }}
                    register("roomConvention") {{
                        id = "{slug}.room"
                        implementationClass = "AndroidRoomPlugin"
                    }}
                    register("hiltConvention") {{
                        id = "{slug}.hilt"
                        implementationClass = "HiltConventionPlugin"
                    }}
                    register("androidModuleConvention") {{
                        id = "{slug}.module"
                        implementationClass = "AndroidModuleConvention"
                    }}
                }}
            }}
            """
        ),
    )


def create_build_logic_classes(root: Path, slug: str) -> None:
    base = root / "build-logic" / "convention" / "src" / "main" / "java"
    write_file(
        base / "AndroidApplicationComposePlugin.kt",
        dedent(
            f"""
            import com.android.build.api.dsl.ApplicationExtension
            import org.gradle.api.Plugin
            import org.gradle.api.Project
            import org.gradle.kotlin.dsl.apply
            import org.gradle.kotlin.dsl.dependencies
            import org.gradle.kotlin.dsl.getByType

            class AndroidApplicationComposePlugin : Plugin<Project> {{
                override fun apply(target: Project) {{
                    with(target) {{
                        apply(plugin = "com.android.application")
                        apply(plugin = "org.jetbrains.kotlin.plugin.compose")

                        val extension = extensions.getByType<ApplicationExtension>()
                        configAndroidCompose(extension)

                        dependencies {{
                            add("implementation", project(":resources"))
                            add("implementation", project(":core:model"))
                            add("implementation", libs.findLibrary("androidx-core-ktx").get())
                            add("implementation", libs.findLibrary("androidx-appcompat").get())
                            add("implementation", libs.findLibrary("androidx-navigation-compose").get())
                        }}
                    }}
                }}
            }}
            """
        ),
    )
    write_file(
        base / "AndroidLibraryComposePlugin.kt",
        dedent(
            f"""
            import com.android.build.api.dsl.LibraryExtension
            import org.gradle.api.Plugin
            import org.gradle.api.Project
            import org.gradle.kotlin.dsl.apply
            import org.gradle.kotlin.dsl.getByType

            class AndroidLibraryComposePlugin : Plugin<Project> {{
                override fun apply(target: Project) {{
                    with(target) {{
                        apply(plugin = "{slug}.module")
                        apply(plugin = "org.jetbrains.kotlin.plugin.compose")

                        val extension = extensions.getByType<LibraryExtension>()
                        configAndroidCompose(extension)
                    }}
                }}
            }}
            """
        ),
    )
    write_file(
        base / "AndroidFeaturePlugin.kt",
        dedent(
            f"""
            import org.gradle.api.Plugin
            import org.gradle.api.Project
            import org.gradle.kotlin.dsl.dependencies

            class AndroidFeaturePlugin : Plugin<Project> {{
                override fun apply(target: Project) {{
                    with(target) {{
                        pluginManager.apply {{
                            apply("{slug}.compose.module")
                            apply("{slug}.hilt")
                            apply("org.jetbrains.kotlin.plugin.serialization")
                        }}

                        dependencies {{
                            add("implementation", project(":resources"))
                            add("implementation", project(":core:model"))
                            add("implementation", libs.findLibrary("androidx-navigation-compose").get())
                        }}
                    }}
                }}
            }}
            """
        ),
    )
    write_file(
        base / "AndroidModuleConvention.kt",
        dedent(
            """
            import com.android.build.gradle.LibraryExtension
            import org.gradle.api.JavaVersion
            import org.gradle.api.Plugin
            import org.gradle.api.Project
            import org.gradle.api.plugins.JavaPluginExtension
            import org.gradle.kotlin.dsl.configure
            import org.gradle.kotlin.dsl.dependencies
            import org.jetbrains.kotlin.gradle.dsl.JvmTarget
            import org.jetbrains.kotlin.gradle.dsl.KotlinAndroidProjectExtension

            class AndroidModuleConvention : Plugin<Project> {
                override fun apply(target: Project) {
                    with(target) {
                        pluginManager.apply("com.android.library")
                        val kotlin = "org.jetbrains.kotlin.android"
                        if (!plugins.hasPlugin(kotlin)) {
                            pluginManager.apply(kotlin)
                        }
                        extensions.configure<LibraryExtension> {
                            compileSdk = 36
                            compileOptions {
                                sourceCompatibility = JavaVersion.VERSION_17
                                targetCompatibility = JavaVersion.VERSION_17
                            }

                            defaultConfig {
                                minSdk = 26
                                testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
                            }
                        }
                        extensions.configure<JavaPluginExtension> {
                            sourceCompatibility = JavaVersion.VERSION_17
                            targetCompatibility = JavaVersion.VERSION_17
                        }

                        configure<KotlinAndroidProjectExtension> {
                            compilerOptions {
                                jvmTarget.set(JvmTarget.JVM_17)
                            }
                        }
                        dependencies {
                            add("implementation", libs.findLibrary("androidx-core-ktx").get())
                            add("implementation", libs.findLibrary("androidx-appcompat").get())
                        }
                    }
                }
            }
            """
        ),
    )
    write_file(
        base / "HiltConventionPlugin.kt",
        dedent(
            """
            import org.gradle.api.Plugin
            import org.gradle.api.Project
            import org.gradle.kotlin.dsl.dependencies

            class HiltConventionPlugin : Plugin<Project> {
                override fun apply(target: Project) {
                    with(target) {
                        pluginManager.apply {
                            apply("com.google.devtools.ksp")
                            apply("com.google.dagger.hilt.android")
                        }

                        dependencies {
                            add("implementation", libs.findLibrary("hilt-android").get())
                            add("implementation", libs.findLibrary("androidx-hilt-navigation-compose").get())
                            add("ksp", libs.findLibrary("dagger-hilt-complier").get())
                            add("ksp", libs.findLibrary("androidx-hilt-complier").get())
                        }
                    }
                }
            }
            """
        ),
    )
    write_file(
        base / "AndroidRoomPlugin.kt",
        dedent(
            """
            import androidx.room.gradle.RoomExtension
            import org.gradle.api.Plugin
            import org.gradle.api.Project
            import org.gradle.kotlin.dsl.configure
            import org.gradle.kotlin.dsl.dependencies

            class AndroidRoomPlugin : Plugin<Project> {
                override fun apply(target: Project) {
                    with(target) {
                        pluginManager.apply {
                            apply("com.google.devtools.ksp")
                            apply("androidx.room")
                        }

                        configure<RoomExtension> {
                            schemaDirectory("$projectDir/schemas")
                        }

                        dependencies {
                            add("implementation", libs.findLibrary("androidx-room-runtime").get())
                            add("implementation", libs.findLibrary("androidx-room-ktx").get())
                            add("ksp", libs.findLibrary("androidx-room-compiler").get())
                        }
                    }
                }
            }
            """
        ),
    )
    write_file(
        base / "AndroidCompose.kt",
        dedent(
            """
            import com.android.build.api.dsl.CommonExtension
            import org.gradle.api.Project
            import org.gradle.api.plugins.ExtensionAware
            import org.gradle.kotlin.dsl.the
            import org.gradle.accessors.dm.LibrariesForLibs

            internal val Project.libs: LibrariesForLibs
                get() = the()

            fun configAndroidCompose(
                commonExtension: CommonExtension<*, *, *, *, *, *>
            ) {
                commonExtension.apply {
                    buildFeatures.compose = true
                    composeOptions.kotlinCompilerExtensionVersion = "1.5.15"
                    defaultConfig {
                        vectorDrawables.useSupportLibrary = true
                    }
                }
            }
            """
        ),
    )


def create_module_common(root: Path, module_dir: str, namespace: str, plugin_alias: str, extra_dependencies: str = "") -> None:
    module_path = root / module_dir
    write_file(
        module_path / "build.gradle.kts",
        module_build_common(namespace, plugin_alias)
        + ("\n\ndependencies {\n" + extra_dependencies.rstrip() + "\n}\n" if extra_dependencies.strip() else "\n"),
    )
    touch_text_file(module_path / "consumer-rules.pro")
    touch_text_file(module_path / "proguard-rules.pro")
    write_file(module_path / "src" / "main" / "AndroidManifest.xml", "<manifest />")


def create_shared_modules(root: Path, base_package: str, slug: str) -> None:
    create_module_common(
        root,
        "resources",
        f"{base_package}.resources",
        f"{slug}-module",
    )
    write_file(
        root / "resources" / "src" / "main" / "res" / "values" / "strings.xml",
        dedent(
            """
            <resources>
                <string name="app_name">Starter App</string>
            </resources>
            """
        ),
    )

    create_module_common(root, "core/model", f"{base_package}.core.model", f"{slug}-module")
    write_file(
        root / "core" / "model" / "src" / "main" / "java" / package_to_path(f"{base_package}.core.model") / "UserSession.kt",
        dedent(
            f"""
            package {base_package}.core.model

            data class UserSession(
                val userId: String = "",
                val accessToken: String = "",
            )
            """
        ),
    )

    create_module_common(
        root,
        "core/theme",
        f"{base_package}.core.theme",
        f"{slug}-compose-module",
        '    implementation(platform(libs.androidx.compose.bom))\n'
        '    implementation(libs.androidx.material3)\n'
        '    implementation(libs.androidx.ui)\n'
        '    implementation(libs.androidx.ui.graphics)\n'
        '    implementation(libs.androidx.ui.tooling.preview)',
    )
    theme_package_path = root / "core" / "theme" / "src" / "main" / "java" / package_to_path(f"{base_package}.core.theme")
    write_file(
        theme_package_path / "Theme.kt",
        dedent(
            f"""
            package {base_package}.core.theme

            import androidx.compose.material3.MaterialTheme
            import androidx.compose.material3.lightColorScheme
            import androidx.compose.runtime.Composable

            private val LightColors = lightColorScheme()

            @Composable
            fun AppTheme(content: @Composable () -> Unit) {{
                MaterialTheme(
                    colorScheme = LightColors,
                    content = content
                )
            }}
            """
        ),
    )

    create_module_common(
        root,
        "core/ui",
        f"{base_package}.core.ui",
        f"{slug}-compose-module",
        '    implementation(platform(libs.androidx.compose.bom))\n'
        '    implementation(libs.androidx.material3)\n'
        '    implementation(libs.androidx.ui)',
    )
    ui_package = root / "core" / "ui" / "src" / "main" / "java" / package_to_path(f"{base_package}.core.ui")
    write_file(
        ui_package / "util" / "LocationStateHolder.kt",
        dedent(
            f"""
            package {base_package}.core.ui.util

            import kotlinx.coroutines.flow.MutableStateFlow
            import kotlinx.coroutines.flow.StateFlow
            import kotlinx.coroutines.flow.asStateFlow

            class LocationStateHolder {{
                private val _currentAddress = MutableStateFlow<String?>(null)
                val currentAddress: StateFlow<String?> = _currentAddress.asStateFlow()

                fun updateAddress(address: String?) {{
                    _currentAddress.value = address
                }}
            }}
            """
        ),
    )

    create_module_common(
        root,
        "core/network",
        f"{base_package}.core.network",
        f"{slug}-module",
    )
    network_build = root / "core" / "network" / "build.gradle.kts"
    network_build.write_text(
        network_build.read_text(encoding="utf-8").replace(
            f'plugins {{\n    alias({plugin_ref(f"{slug}-module")})\n    alias({plugin_ref(f"{slug}-hilt")})\n}}\n\nandroid {{\n    namespace = "{base_package}.core.network"\n}}\n',
            dedent(
                f"""
                plugins {{
                    alias({plugin_ref(f"{slug}-module")})
                    alias({plugin_ref(f"{slug}-hilt")})
                }}

                android {{
                    namespace = "{base_package}.core.network"

                    buildFeatures {{
                        buildConfig = true
                    }}

                    defaultConfig {{
                        val apiBaseUrl = (findProperty("api.baseUrl") as String?)
                            ?: System.getenv("API_BASE_URL")
                            ?: "https://api.example.com"
                        buildConfigField("String", "API_BASE_URL", "\\"${{apiBaseUrl.trimEnd('/')}}\\"")
                    }}
                }}

                dependencies {{
                    implementation(projects.core.model)
                    implementation(libs.ktor.serialization.kotlinx.json)
                    implementation("io.ktor:ktor-client-core:2.3.12")
                    implementation("io.ktor:ktor-client-android:2.3.12")
                    implementation("io.ktor:ktor-client-okhttp:2.3.12")
                    implementation("io.ktor:ktor-client-content-negotiation:2.3.12")
                }}
                """
            ),
        ),
        encoding="utf-8",
    )
    network_package = root / "core" / "network" / "src" / "main" / "java" / package_to_path(f"{base_package}.core.network")
    write_file(
        network_package / "NetworkModule.kt",
        dedent(
            f"""
            package {base_package}.core.network

            import dagger.Module
            import dagger.Provides
            import dagger.hilt.InstallIn
            import dagger.hilt.components.SingletonComponent
            import io.ktor.client.HttpClient
            import io.ktor.client.engine.okhttp.OkHttp
            import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
            import io.ktor.client.plugins.defaultRequest
            import io.ktor.serialization.kotlinx.json.json
            import javax.inject.Named
            import javax.inject.Singleton
            import kotlinx.serialization.json.Json

            @Module
            @InstallIn(SingletonComponent::class)
            object NetworkModule {{
                private const val API_BASE_URL = BuildConfig.API_BASE_URL

                @Provides
                @Singleton
                @Named("auth")
                fun provideAuthHttpClient(): HttpClient {{
                    return HttpClient(OkHttp) {{
                        defaultRequest {{
                            url("$API_BASE_URL/api/auth/")
                        }}
                        install(ContentNegotiation) {{
                            json(Json {{ ignoreUnknownKeys = true }})
                        }}
                    }}
                }}
            }}
            """
        ),
    )
    write_file(
        network_package / "NetworkDataSource.kt",
        dedent(
            f"""
            package {base_package}.core.network

            import io.ktor.client.HttpClient
            import javax.inject.Inject
            import javax.inject.Named

            class NetworkDataSource @Inject constructor(
                @Named("auth") private val authClient: HttpClient,
            )
            """
        ),
    )

    create_module_common(
        root,
        "core/data",
        f"{base_package}.core.data",
        f"{slug}-module",
    )
    data_build = root / "core" / "data" / "build.gradle.kts"
    data_build.write_text(
        dedent(
            f"""
            plugins {{
                alias({plugin_ref(f"{slug}-module")})
                alias({plugin_ref(f"{slug}-hilt")})
            }}

            android {{
                namespace = "{base_package}.core.data"
            }}

            dependencies {{
                implementation(projects.core.network)
                implementation(projects.core.datastore)
                implementation(projects.core.database)
                implementation(projects.core.model)
            }}
            """
        ),
        encoding="utf-8",
    )
    data_package = root / "core" / "data" / "src" / "main" / "java" / package_to_path(f"{base_package}.core.data")
    write_file(
        data_package / "repository" / "AuthRepository.kt",
        dedent(
            f"""
            package {base_package}.core.data.repository

            import kotlinx.coroutines.flow.Flow

            interface AuthRepository {{
                val isLoggedIn: Flow<Boolean>
                suspend fun getToken(): String?
            }}
            """
        ),
    )
    write_file(
        data_package / "impl" / "AuthRepositoryImpl.kt",
        dedent(
            f"""
            package {base_package}.core.data.impl

            import {base_package}.core.data.repository.AuthRepository
            import {base_package}.core.datastore.AuthDataStore
            import javax.inject.Inject
            import javax.inject.Singleton
            import kotlinx.coroutines.flow.Flow

            @Singleton
            class AuthRepositoryImpl @Inject constructor(
                private val authDataStore: AuthDataStore
            ) : AuthRepository {{
                override val isLoggedIn: Flow<Boolean> = authDataStore.isLoggedInFlow()

                override suspend fun getToken(): String? = authDataStore.getToken()
            }}
            """
        ),
    )
    write_file(
        data_package / "di" / "DataModule.kt",
        dedent(
            f"""
            package {base_package}.core.data.di

            import {base_package}.core.data.impl.AuthRepositoryImpl
            import {base_package}.core.data.repository.AuthRepository
            import dagger.Binds
            import dagger.Module
            import dagger.hilt.InstallIn
            import dagger.hilt.components.SingletonComponent
            import javax.inject.Singleton

            @Module
            @InstallIn(SingletonComponent::class)
            abstract class DataModule {{
                @Binds
                @Singleton
                abstract fun bindAuthRepository(
                    impl: AuthRepositoryImpl
                ): AuthRepository
            }}
            """
        ),
    )

    create_module_common(
        root,
        "core/database",
        f"{base_package}.core.database",
        f"{slug}-module",
    )
    database_build = root / "core" / "database" / "build.gradle.kts"
    database_build.write_text(
        dedent(
            f"""
            plugins {{
                alias({plugin_ref(f"{slug}-module")})
                alias({plugin_ref(f"{slug}-room")})
                alias({plugin_ref(f"{slug}-hilt")})
            }}

            android {{
                namespace = "{base_package}.core.database"
            }}

            dependencies {{
                implementation(libs.androidx.room.runtime)
                implementation(libs.androidx.room.ktx)
                ksp(libs.androidx.room.compiler)
            }}
            """
        ),
        encoding="utf-8",
    )
    db_package = root / "core" / "database" / "src" / "main" / "java" / package_to_path(f"{base_package}.core.database")
    write_file(
        db_package / "AgriDoctorDatabase.kt",
        dedent(
            f"""
            package {base_package}.core.database

            import androidx.room.Database
            import androidx.room.RoomDatabase
            import {base_package}.core.database.dao.PlaceholderDao
            import {base_package}.core.database.model.PlaceholderEntity

            @Database(
                entities = [PlaceholderEntity::class],
                version = 1,
                exportSchema = false
            )
            abstract class AppDatabase : RoomDatabase() {{
                abstract fun placeholderDao(): PlaceholderDao
            }}
            """
        ),
    )
    write_file(
        db_package / "model" / "PlaceholderEntity.kt",
        dedent(
            f"""
            package {base_package}.core.database.model

            import androidx.room.Entity
            import androidx.room.PrimaryKey

            @Entity(tableName = "placeholder")
            data class PlaceholderEntity(
                @PrimaryKey val id: Long = 0
            )
            """
        ),
    )
    write_file(
        db_package / "dao" / "PlaceholderDao.kt",
        dedent(
            f"""
            package {base_package}.core.database.dao

            import androidx.room.Dao
            import androidx.room.Query
            import {base_package}.core.database.model.PlaceholderEntity
            import kotlinx.coroutines.flow.Flow

            @Dao
            interface PlaceholderDao {{
                @Query("SELECT * FROM placeholder")
                fun getAll(): Flow<List<PlaceholderEntity>>
            }}
            """
        ),
    )
    write_file(
        db_package / "di" / "DatabaseModule.kt",
        dedent(
            f"""
            package {base_package}.core.database.di

            import android.content.Context
            import androidx.room.Room
            import {base_package}.core.database.AppDatabase
            import dagger.Module
            import dagger.Provides
            import dagger.hilt.InstallIn
            import dagger.hilt.android.qualifiers.ApplicationContext
            import dagger.hilt.components.SingletonComponent
            import javax.inject.Singleton

            @Module
            @InstallIn(SingletonComponent::class)
            object DatabaseModule {{
                @Provides
                @Singleton
                fun provideDatabase(
                    @ApplicationContext context: Context
                ): AppDatabase {{
                    return Room.databaseBuilder(
                        context,
                        AppDatabase::class.java,
                        "app_database"
                    ).build()
                }}
            }}
            """
        ),
    )

    datastore_path = root / "core" / "datastore"
    write_file(
        datastore_path / "build.gradle.kts",
        dedent(
            f"""
            plugins {{
                alias({plugin_ref(f"{slug}-compose-module")})
                alias(libs.plugins.google.protobuf)
            }}

            android {{
                namespace = "{base_package}.core.datastore"
            }}

            dependencies {{
                implementation(libs.androidx.datastore)
                implementation(libs.protobuf.kotlin.lite)
            }}

            protobuf {{
                protoc {{
                    artifact = libs.protobuf.protoc.get().toString()
                }}
                generateProtoTasks {{
                    all().forEach {{ task ->
                        task.builtins {{
                            create("java") {{
                                option("lite")
                            }}
                        }}
                    }}
                }}
            }}
            """
        ),
    )
    touch_text_file(datastore_path / "consumer-rules.pro")
    touch_text_file(datastore_path / "proguard-rules.pro")
    write_file(datastore_path / "src" / "main" / "AndroidManifest.xml", "<manifest />")
    write_file(
        datastore_path / "src" / "main" / "proto" / "auth.proto",
        dedent(
            f"""
            syntax = "proto3";

            option java_package = "{base_package}.core.datastore";
            option java_multiple_files = true;

            message AuthProto {{
              string jwt_token = 1;
              int64 timestamp = 2;
              string user_id = 3;
            }}
            """
        ),
    )
    datastore_package = datastore_path / "src" / "main" / "java" / package_to_path(f"{base_package}.core.datastore")
    write_file(
        datastore_package / "AuthDataStore.kt",
        dedent(
            f"""
            package {base_package}.core.datastore

            import android.content.Context
            import androidx.datastore.core.DataStore
            import androidx.datastore.core.Serializer
            import androidx.datastore.dataStore
            import dagger.hilt.android.qualifiers.ApplicationContext
            import java.io.IOException
            import java.io.InputStream
            import java.io.OutputStream
            import javax.inject.Inject
            import kotlinx.coroutines.flow.Flow
            import kotlinx.coroutines.flow.catch
            import kotlinx.coroutines.flow.first
            import kotlinx.coroutines.flow.map

            class AuthDataStore @Inject constructor(
                @ApplicationContext context: Context,
            ) {{
                private val appContext = context.applicationContext
                private val authDataStore: DataStore<AuthProto> = appContext.authDataStore

                suspend fun getToken(): String? {{
                    return authDataStore.data.first().jwtToken.takeIf {{ it.isNotBlank() }}
                }}

                fun isLoggedInFlow(): Flow<Boolean> = authDataStore.data
                    .catch {{ if (it is IOException) emit(AuthProto.getDefaultInstance()) else throw it }}
                    .map {{ it.jwtToken.isNotBlank() }}
            }}

            private object AuthProtoSerializer : Serializer<AuthProto> {{
                override val defaultValue: AuthProto = AuthProto.getDefaultInstance()

                override suspend fun readFrom(input: InputStream): AuthProto {{
                    return try {{
                        AuthProto.parseFrom(input)
                    }} catch (error: IOException) {{
                        throw androidx.datastore.core.CorruptionException("Cannot read auth proto.", error)
                    }}
                }}

                override suspend fun writeTo(t: AuthProto, output: OutputStream) {{
                    t.writeTo(output)
                }}
            }}

            private val Context.authDataStore: DataStore<AuthProto> by dataStore(
                fileName = "auth.pb",
                serializer = AuthProtoSerializer
            )
            """
        ),
    )

    create_module_common(root, "core/alarm", f"{base_package}.core.alarm", f"{slug}-module")
    alarm_package = root / "core" / "alarm" / "src" / "main" / "java" / package_to_path(f"{base_package}.core.alarm")
    write_file(
        alarm_package / "ReminderAlarmScheduler.kt",
        dedent(
            f"""
            package {base_package}.core.alarm

            object ReminderAlarmScheduler
            """
        ),
    )


def create_app_module(root: Path, project_name: str, base_package: str, slug: str, features: list[str]) -> None:
    app_path = root / "app"
    has_home = "home" in features
    has_login = "login" in features
    signed_in_destination = "HOME_ROUTE" if has_home else ("LOGIN_ROUTE" if has_login else '"main"')
    signed_out_destination = "LOGIN_ROUTE" if has_login else ("HOME_ROUTE" if has_home else '"main"')
    feature_dependencies = []
    if has_home:
        feature_dependencies.append("    implementation(projects.feature.home)")
    if has_login:
        feature_dependencies.append("    implementation(projects.feature.login)")
    feature_dependency_block = "\n".join(feature_dependencies)
    write_file(
        app_path / "build.gradle.kts",
        dedent(
            f"""
            plugins {{
                alias({plugin_ref(f"{slug}-compose-application")})
                alias(libs.plugins.jetbrains.kotlin.android)
                alias({plugin_ref(f"{slug}-hilt")})
            }}

            android {{
                namespace = "{base_package}"
                compileSdk = 36

                defaultConfig {{
                    applicationId = "{base_package}"
                    minSdk = 27
                    targetSdk = 36
                    versionCode = 1
                    versionName = "1.0"
                    testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
                }}

                buildFeatures {{
                    compose = true
                }}
            }}

            dependencies {{
                implementation(platform(libs.androidx.compose.bom))
                implementation(libs.androidx.ui)
                implementation(libs.androidx.ui.graphics)
                implementation(libs.androidx.ui.tooling.preview)
                implementation(libs.androidx.material3)
                implementation(libs.androidx.activity.compose)
                implementation(libs.androidx.lifecycle.runtime.ktx)
                implementation(projects.core.model)
                implementation(projects.core.data)
                implementation(projects.resources)
                implementation(projects.core.ui)
                implementation(projects.core.theme)
            {feature_dependency_block}
            }}
            """
        ),
    )
    touch_text_file(app_path / "proguard-rules.pro")
    app_package = app_path / "src" / "main" / "java" / package_to_path(base_package)
    write_file(
        app_path / "src" / "main" / "AndroidManifest.xml",
        dedent(
            f"""
            <manifest xmlns:android="http://schemas.android.com/apk/res/android">
                <application
                    android:name=".App"
                    android:allowBackup="false"
                    android:label="@string/app_name"
                    android:icon="@mipmap/ic_launcher"
                    android:networkSecurityConfig="@xml/network_security_config"
                    android:supportsRtl="true"
                    android:theme="@style/Theme.{project_name}"
                    android:usesCleartextTraffic="false">
                    <activity
                        android:name=".MainActivity"
                        android:exported="true">
                        <intent-filter>
                            <action android:name="android.intent.action.MAIN" />
                            <category android:name="android.intent.category.LAUNCHER" />
                        </intent-filter>
                    </activity>
                </application>
            </manifest>
            """
        ),
    )
    write_file(
        app_package / "App.kt",
        dedent(
            f"""
            package {base_package}

            import android.app.Application
            import dagger.hilt.android.HiltAndroidApp

            @HiltAndroidApp
            class App : Application()
            """
        ),
    )
    write_file(
        app_package / "MainViewModel.kt",
        dedent(
            f"""
            package {base_package}

            import androidx.lifecycle.ViewModel
            import androidx.lifecycle.viewModelScope
            import {base_package}.core.data.repository.AuthRepository
            import dagger.hilt.android.lifecycle.HiltViewModel
            import javax.inject.Inject
            import kotlinx.coroutines.flow.SharingStarted
            import kotlinx.coroutines.flow.StateFlow
            import kotlinx.coroutines.flow.map
            import kotlinx.coroutines.flow.stateIn

            @HiltViewModel
            class MainViewModel @Inject constructor(
                authRepository: AuthRepository
            ) : ViewModel() {{
                val isLoggedIn: StateFlow<Boolean> = authRepository.isLoggedIn
                    .map {{ it }}
                    .stateIn(
                        scope = viewModelScope,
                        started = SharingStarted.WhileSubscribed(5_000),
                        initialValue = false
                    )
            }}
            """
        ),
    )
    write_file(
        app_package / "MainActivity.kt",
        dedent(
            f"""
            package {base_package}

            import android.os.Bundle
            import androidx.activity.ComponentActivity
            import androidx.activity.compose.setContent
            import androidx.activity.enableEdgeToEdge
            import androidx.activity.viewModels
            import androidx.compose.foundation.layout.fillMaxSize
            import androidx.compose.ui.Modifier
            import androidx.lifecycle.compose.collectAsStateWithLifecycle
            import {base_package}.core.theme.AppTheme
            import {base_package}.navigation.rememberAppState
            import {base_package}.ui.MainApp
            import dagger.hilt.android.AndroidEntryPoint

            @AndroidEntryPoint
            class MainActivity : ComponentActivity() {{
                private val mainViewModel: MainViewModel by viewModels()

                override fun onCreate(savedInstanceState: Bundle?) {{
                    super.onCreate(savedInstanceState)
                    enableEdgeToEdge()
                    setContent {{
                        val isLoggedIn = mainViewModel.isLoggedIn.collectAsStateWithLifecycle().value
                        val appState = rememberAppState()

                        AppTheme {{
                            MainApp(
                                modifier = Modifier.fillMaxSize(),
                                appState = appState,
                                startDestination = if (isLoggedIn) {signed_in_destination} else {signed_out_destination}
                            )
                        }}
                    }}
                }}
            }}
            """
        ),
    )
    navigation_package = app_package / "navigation"
    write_file(
        navigation_package / "TopLevelDestination.kt",
        dedent(
            f"""
            package {base_package}.navigation

            {f'import {base_package}.feature.home.navigation.HOME_ROUTE' if has_home else ''}

            enum class TopLevelDestination(
                val route: String
            ) {{
                {f'HOME(route = HOME_ROUTE)' if has_home else 'MAIN(route = "main")'}
            }}
            """
        ),
    )
    write_file(
        navigation_package / "AppState.kt",
        dedent(
            f"""
            package {base_package}.navigation

            import androidx.compose.runtime.Composable
            import androidx.compose.runtime.remember
            import androidx.navigation.NavHostController
            import androidx.navigation.compose.rememberNavController
            import {base_package}.core.ui.util.LocationStateHolder

            class AppState(
                val navController: NavHostController,
                val locationStateHolder: LocationStateHolder
            )

            @Composable
            fun rememberAppState(): AppState {{
                val navController = rememberNavController()
                val locationStateHolder = remember {{ LocationStateHolder() }}
                return remember(navController, locationStateHolder) {{
                    AppState(navController, locationStateHolder)
                }}
            }}
            """
        ),
    )
    write_file(
        navigation_package / "MainNavHost.kt",
        dedent(
            f"""
            package {base_package}.navigation

            import androidx.compose.runtime.Composable
            import androidx.compose.ui.Modifier
            import androidx.navigation.compose.NavHost
            {"import " + base_package + ".feature.home.navigation.HOME_ROUTE" if has_home else ""}
            {"import " + base_package + ".feature.home.navigation.homeScreen" if has_home else ""}
            {"import " + base_package + ".feature.home.navigation.navigateToHome" if has_home else ""}
            {"import " + base_package + ".feature.login.navigation.LOGIN_ROUTE" if has_login else ""}
            {"import " + base_package + ".feature.login.navigation.loginScreen" if has_login else ""}
            {"import " + base_package + ".feature.login.navigation.navigateToLogin" if has_login else ""}

            @Composable
            fun MainNavHost(
                modifier: Modifier = Modifier,
                appState: AppState,
                startDestination: String = {signed_out_destination}
            ) {{
                NavHost(
                    modifier = modifier,
                    navController = appState.navController,
                    startDestination = startDestination
                ) {{
                    {dedent(f'''
                    loginScreen(
                        onNavigateToHome = appState.navController::navigateToHome,
                    )
                    ''' ).strip() if has_login and has_home else ""}
                    {dedent(f'''
                    homeScreen(
                        onNavigateToLogin = appState.navController::navigateToLogin,
                    )
                    ''' ).strip() if has_home and has_login else ""}
                    {dedent(f'''
                    homeScreen(
                        onNavigateToLogin = {{}},
                    )
                    ''' ).strip() if has_home and not has_login else ""}
                    {dedent(f'''
                    loginScreen(
                        onNavigateToHome = {{}},
                    )
                    ''' ).strip() if has_login and not has_home else ""}
                }}
            }}
            """
        ),
    )
    ui_package = app_package / "ui"
    write_file(
        ui_package / "MainApp.kt",
        dedent(
            f"""
            package {base_package}.ui

            import androidx.compose.runtime.Composable
            import androidx.compose.ui.Modifier
            import {base_package}.navigation.AppState
            import {base_package}.navigation.MainNavHost

            @Composable
            fun MainApp(
                modifier: Modifier = Modifier,
                appState: AppState,
                startDestination: String
            ) {{
                MainNavHost(
                    modifier = modifier,
                    appState = appState,
                    startDestination = startDestination
                )
            }}
            """
        ),
    )
    write_file(
        ui_package / "MainBottomNavBar.kt",
        dedent(
            f"""
            package {base_package}.ui

            import androidx.compose.runtime.Composable

            @Composable
            fun MainBottomNavBar() = Unit
            """
        ),
    )
    write_file(
        app_path / "src" / "main" / "res" / "values" / "strings.xml",
        dedent(
            f"""
            <resources>
                <string name="app_name">{project_name}</string>
            </resources>
            """
        ),
    )
    write_file(
        app_path / "src" / "main" / "res" / "values" / "themes.xml",
        dedent(
            f"""
            <resources xmlns:tools="http://schemas.android.com/tools">
                <style name="Theme.{project_name}" parent="Theme.Material3.DayNight.NoActionBar" />
            </resources>
            """
        ),
    )
    write_file(
        app_path / "src" / "main" / "res" / "xml" / "network_security_config.xml",
        dedent(
            """
            <?xml version="1.0" encoding="utf-8"?>
            <network-security-config>
                <base-config cleartextTrafficPermitted="false">
                    <trust-anchors>
                        <certificates src="system" />
                    </trust-anchors>
                </base-config>
            </network-security-config>
            """
        ),
    )


def create_feature_module(root: Path, base_package: str, slug: str, name: str) -> None:
    feature_name = name.strip().lower()
    pascal = feature_pascal(feature_name)
    camel = feature_camel(feature_name)
    namespace = f"{base_package}.feature.{feature_name}"
    module_path = root / "feature" / feature_name
    write_file(
        module_path / "build.gradle.kts",
        dedent(
            f"""
            plugins {{
                alias({plugin_ref(f"{slug}-feature")})
            }}

            android {{
                namespace = "{namespace}"
            }}

            dependencies {{
                implementation(projects.core.theme)
                implementation(projects.core.data)
                implementation(projects.core.ui)
            }}
            """
        ),
    )
    touch_text_file(module_path / "consumer-rules.pro")
    touch_text_file(module_path / "proguard-rules.pro")
    write_file(module_path / "src" / "main" / "AndroidManifest.xml", "<manifest />")
    feature_package = module_path / "src" / "main" / "java" / package_to_path(namespace)
    route_name = f"{feature_name}"
    route_constant = f"{feature_name.upper()}_ROUTE"

    if feature_name == "login":
        screen_content = dedent(
            f"""
            package {namespace}

            import androidx.compose.foundation.layout.Arrangement
            import androidx.compose.foundation.layout.Column
            import androidx.compose.foundation.layout.fillMaxSize
            import androidx.compose.material3.Button
            import androidx.compose.material3.Text
            import androidx.compose.runtime.Composable
            import androidx.compose.ui.Alignment
            import androidx.compose.ui.Modifier
            import androidx.hilt.navigation.compose.hiltViewModel
            import androidx.lifecycle.compose.collectAsStateWithLifecycle

            @Composable
            fun {pascal}Route(
                onNavigateToHome: () -> Unit,
                viewModel: {pascal}ViewModel = hiltViewModel()
            ) {{
                val uiState = viewModel.uiState.collectAsStateWithLifecycle().value

                {pascal}Screen(
                    isLoading = uiState.isLoading,
                    onLoginClick = onNavigateToHome
                )
            }}

            @Composable
            fun {pascal}Screen(
                isLoading: Boolean,
                onLoginClick: () -> Unit
            ) {{
                Column(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {{
                    Text("Login")
                    Button(onClick = onLoginClick, enabled = !isLoading) {{
                        Text("Continue")
                    }}
                }}
            }}
            """
        )
        nav_extra_signature = "    onNavigateToHome: () -> Unit\n"
        nav_call = f"        {pascal}Route(onNavigateToHome = onNavigateToHome)\n"
    elif feature_name == "home":
        screen_content = dedent(
            f"""
            package {namespace}

            import androidx.compose.foundation.layout.Arrangement
            import androidx.compose.foundation.layout.Column
            import androidx.compose.foundation.layout.fillMaxSize
            import androidx.compose.material3.Button
            import androidx.compose.material3.Text
            import androidx.compose.runtime.Composable
            import androidx.compose.ui.Alignment
            import androidx.compose.ui.Modifier
            import androidx.hilt.navigation.compose.hiltViewModel
            import androidx.lifecycle.compose.collectAsStateWithLifecycle
            import {namespace}.component.{pascal}Content

            @Composable
            fun {pascal}Route(
                onNavigateToLogin: () -> Unit,
                viewModel: {pascal}ViewModel = hiltViewModel()
            ) {{
                val uiState = viewModel.uiState.collectAsStateWithLifecycle().value

                {pascal}Screen(
                    title = uiState.title,
                    onNavigateToLogin = onNavigateToLogin
                )
            }}

            @Composable
            fun {pascal}Screen(
                title: String,
                onNavigateToLogin: () -> Unit
            ) {{
                Column(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {{
                    {pascal}Content(title = title)
                    Button(onClick = onNavigateToLogin) {{
                        Text("Go to login")
                    }}
                }}
            }}
            """
        )
        nav_extra_signature = "    onNavigateToLogin: () -> Unit\n"
        nav_call = f"        {pascal}Route(onNavigateToLogin = onNavigateToLogin)\n"
    else:
        screen_content = dedent(
            f"""
            package {namespace}

            import androidx.compose.foundation.layout.Arrangement
            import androidx.compose.foundation.layout.Column
            import androidx.compose.foundation.layout.fillMaxSize
            import androidx.compose.material3.Text
            import androidx.compose.runtime.Composable
            import androidx.compose.ui.Alignment
            import androidx.compose.ui.Modifier
            import androidx.hilt.navigation.compose.hiltViewModel
            import androidx.lifecycle.compose.collectAsStateWithLifecycle
            import {namespace}.component.{pascal}Content

            @Composable
            fun {pascal}Route(
                viewModel: {pascal}ViewModel = hiltViewModel()
            ) {{
                val uiState = viewModel.uiState.collectAsStateWithLifecycle().value

                {pascal}Screen(
                    title = uiState.title
                )
            }}

            @Composable
            fun {pascal}Screen(
                title: String
            ) {{
                Column(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {{
                    {pascal}Content(title = title)
                }}
            }}
            """
        )
        nav_extra_signature = ""
        nav_call = f"        {pascal}Route()\n"

    write_file(feature_package / f"{pascal}Screen.kt", screen_content)
    write_file(
        feature_package / f"{pascal}ViewModel.kt",
        dedent(
            f"""
            package {namespace}

            import androidx.lifecycle.ViewModel
            import dagger.hilt.android.lifecycle.HiltViewModel
            import javax.inject.Inject
            import kotlinx.coroutines.flow.MutableStateFlow
            import kotlinx.coroutines.flow.StateFlow
            import kotlinx.coroutines.flow.asStateFlow

            data class {pascal}UiState(
                val title: String = "{pascal}",
                val isLoading: Boolean = false
            )

            @HiltViewModel
            class {pascal}ViewModel @Inject constructor() : ViewModel() {{
                private val _uiState = MutableStateFlow({pascal}UiState())
                val uiState: StateFlow<{pascal}UiState> = _uiState.asStateFlow()
            }}
            """
        ),
    )
    write_file(
        feature_package / "component" / f"{pascal}Content.kt",
        dedent(
            f"""
            package {namespace}.component

            import androidx.compose.material3.Text
            import androidx.compose.runtime.Composable

            @Composable
            fun {pascal}Content(title: String) {{
                Text(title)
            }}
            """
        ),
    )
    write_file(
        feature_package / "navigation" / f"{pascal}Navigation.kt",
        dedent(
            f"""
            package {namespace}.navigation

            import androidx.navigation.NavController
            import androidx.navigation.NavGraphBuilder
            import androidx.navigation.NavOptions
            import androidx.navigation.compose.composable
            import {namespace}.{pascal}Route

            const val {route_constant} = "{route_name}"

            fun NavController.navigateTo{pascal}(navOptions: NavOptions? = null) {{
                navigate({route_constant}, navOptions)
            }}

            fun NavGraphBuilder.{camel}Screen(
            {nav_extra_signature}) {{
                composable(route = {route_constant}) {{
            {nav_call.rstrip()}
                }}
            }}
            """
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold an AgriDoctorAI-style Android project.")
    parser.add_argument("--output", required=True, help="Output directory for the new project")
    parser.add_argument("--project-name", required=True, help="Project name")
    parser.add_argument("--package", required=True, dest="base_package", help="Base package name")
    parser.add_argument("--slug", required=False, help="Short slug for plugin ids")
    parser.add_argument("--features", default="home,login", help="Comma-separated starter features")
    parser.add_argument("--minimal", action="store_true", help="Create baseline modules only")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.output).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    slug = slugify(args.slug or args.project_name)
    features = [] if args.minimal else [item.strip() for item in args.features.split(",") if item.strip()]

    shared_modules = [
        ":app",
        ":resources",
        ":core:model",
        ":core:theme",
        ":core:ui",
        ":core:network",
        ":core:data",
        ":core:database",
        ":core:datastore",
        ":core:alarm",
    ]
    feature_modules = [f":feature:{name}" for name in features]

    create_root_files(root, args.project_name, slug, shared_modules + feature_modules)
    create_build_logic_classes(root, slug)
    create_shared_modules(root, args.base_package, slug)
    create_app_module(root, args.project_name, args.base_package, slug, features)
    for feature in features:
        create_feature_module(root, args.base_package, slug, feature)

    print(f"Scaffolded project at: {root}")
    print(f"Slug: {slug}")
    if features:
        print(f"Features: {', '.join(features)}")
    else:
        print("Features: none (minimal mode)")


if __name__ == "__main__":
    main()
