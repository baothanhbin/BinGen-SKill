# Skill Gen App Compose Multi Module

Skill Codex de scaffold mot Android project moi theo cau truc Compose multi-module, bam style to chuc cua `AgriDoctorAI`.

## Repo layout

```text
skills/
  skill-gen-app-compose-multi-module/
    SKILL.md
    agents/
    references/
    scripts/
```

## Cai bang CLI kieu `npx skills add`

Repo nay da theo layout `skills/...`, nen Codex CLI co the quet truc tiep dung kieu skills repo.

Cai toan bo skill co trong repo:

```powershell
npx skills add https://github.com/baothanhbin/BinGen-SKill
```

Hoac chi dinh dung skill can cai:

```powershell
npx skills add https://github.com/baothanhbin/BinGen-SKill --skill "skill-gen-app-compose-multi-module"
```

Sau khi cai, restart Codex de skill moi duoc load.

## Cai thu cong vao Codex

Copy folder nay vao:

```text
%USERPROFILE%\.codex\skills\skill-gen-app-compose-multi-module
```

Folder can copy la:

```text
skills/skill-gen-app-compose-multi-module
```

## Cach goi trong Codex

```text
Use $skill-gen-app-compose-multi-module to scaffold a new Android project with a Compose multi-module architecture.
```
