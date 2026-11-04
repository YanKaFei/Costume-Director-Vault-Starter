#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Project-level Look Bible (R1.1-E / AUD-003).

Look Bible lives under projects/<slug>/look-bible/look-bible.json.
Only the project bible is written; public cards (01-09) are read-only here.

Statuses: Draft -> Proposed -> Approved.
Anchors: per-slot lock hard|soft; approved anchors are frozen against silent
overwrite. Approval requires a human reviewer + a signature file (JSON) whose
role is human/reviewer; the agent actor cannot self-approve.

Commands: init/add/patch/propose/approve/diff/validate/list.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "1.0"
STATUSES = ("Draft", "Proposed", "Approved")
CARD_ID_RE = re.compile(r"^(GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC|RUL)-\d{4}$")
AGENT_WORDS = ("agent", "ai", "bot", "assistant", "automated", "llm")


def now():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def root_dir(value):
    return Path(value).resolve() if value else Path(__file__).resolve().parent.parent


def project_dir(root, slug):
    return root / "projects" / slug / "look-bible"


def bible_path(root, slug):
    return project_dir(root, slug) / "look-bible.json"


def loads(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dumps(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=False)
        fh.write("\n")


def load_bible(root, slug):
    path = bible_path(root, slug)
    if not path.exists():
        fail("look-bible not found: %s (run init first)" % path)
    data = loads(path)
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        fail("unsupported look-bible schema_version: %r" % (data.get("schema_version"),))
    data.setdefault("looks", {})
    return data


def save_bible(root, slug, bible):
    bible["updated_at"] = now()
    dumps(bible_path(root, slug), bible)


def get_look(bible, look_id):
    if look_id not in bible["looks"]:
        fail("look not found: %s" % look_id)
    return bible["looks"][look_id]


def snapshot(root, slug, look):
    path = project_dir(root, slug) / "versions" / look["look_id"] / ("v%d.json" % look["version"])
    dumps(path, look)
    return path


def bump(look, actor, action, patch=None, note=""):
    look["version"] = int(look.get("version", 0)) + 1
    look["updated_at"] = now()
    entry = {
        "version": look["version"],
        "at": look["updated_at"],
        "actor": actor,
        "action": action,
        "item_patch": patch or [],
        "note": note or "",
    }
    look.setdefault("change_log", []).append(entry)
    return entry


def fail(message, code=1):
    sys.stderr.write("ERROR: %s\n" % message)
    raise SystemExit(code)


def ok(message):
    print(message)


def cmd_init(args):
    root = root_dir(args.root)
    slug = args.project
    bdir = project_dir(root, slug)
    if bible_path(root, slug).exists() and not args.force:
        fail("look-bible already exists: %s" % bible_path(root, slug))
    bible = {
        "schema_version": SCHEMA_VERSION,
        "project": slug,
        "title": args.title or slug,
        "created_at": now(),
        "updated_at": now(),
        "looks": {},
    }
    dumps(bible_path(root, slug), bible)
    readme = bdir / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Look Bible — %s\n\n项目级 Look Bible（不写入 01–09 公共卡）。\n\n"
            "状态：Draft → Proposed → Approved；Approved 需 human reviewer + signature JSON。\n"
            "anchors：slot 级 lock `hard`/`soft`；Approved 后 hard anchor 不能被静默覆盖。\n"
            "命令：`python3 scripts/lookbook.py init|add|patch|propose|approve|diff|validate --project <slug>`\n",
            encoding="utf-8",
        )
    ok("initialized %s" % bdir)


def cmd_list(args):
    root = root_dir(args.root)
    bible = load_bible(root, args.project)
    for lid, look in sorted(bible["looks"].items()):
        ok("%-18s %-9s v%-3d %s" % (lid, look.get("status"), look.get("version"), look.get("character_id", "")))


def cmd_add(args):
    root = root_dir(args.root)
    bible = load_bible(root, args.project)
    look = bible["looks"].get(args.look)
    created = False
    if look is None:
        if not args.character:
            fail("--character is required when creating a new look")
        look = {
            "character_id": args.character,
            "look_id": args.look,
            "status": "Draft",
            "version": 1,
            "created_at": now(),
            "updated_at": now(),
            "author": args.actor,
            "rationale": args.rationale or "",
            "sources": list(args.source or []),
            "scene_changes": list(args.scene_change or []),
            "slots": {},
            "approved_anchors": {"hard": [], "soft": []},
            "change_log": [],
            "approvals": [],
        }
        bump(look, args.actor, "init", note=args.note or "create look")
        bible["looks"][args.look] = look
        created = True
    if args.slot:
        if not args.card:
            fail("--card is required with --slot")
        if not CARD_ID_RE.match(args.card):
            fail("invalid card id: %s" % args.card)
        existing = look["slots"].get(args.slot)
        approved_hard = {a["slot"] for a in look.get("approved_anchors", {}).get("hard", [])}
        if look.get("status") == "Approved" and existing and args.slot in approved_hard and existing.get("card_id") != args.card:
            fail("approved hard anchor cannot be overwritten: slot=%s card=%s" % (args.slot, existing.get("card_id")))
        lock = args.lock or (existing or {}).get("lock") or "soft"
        if lock not in ("hard", "soft"):
            fail("--lock must be hard or soft")
        look["slots"][args.slot] = {
            "card_id": args.card,
            "lock": lock,
            "note": args.note or (existing or {}).get("note", ""),
        }
        bump(look, args.actor, "add", patch=[{"slot": args.slot, "from": (existing or {}).get("card_id"), "to": args.card}],
             note=args.note or "")
    snapshot(root, args.project, look)
    save_bible(root, args.project, bible)
    ok("%s %s v%d %s" % ("created" if created else "updated", args.look, look["version"], look["status"]))


def cmd_patch(args):
    root = root_dir(args.root)
    bible = load_bible(root, args.project)
    look = get_look(bible, args.look)
    if args.slot not in look["slots"]:
        fail("slot not found: %s" % args.slot)
    if not CARD_ID_RE.match(args.card):
        fail("invalid card id: %s" % args.card)
    old = look["slots"][args.slot]["card_id"]
    approved_hard = {a["slot"] for a in look.get("approved_anchors", {}).get("hard", [])}
    if look.get("status") == "Approved" and args.slot in approved_hard and old != args.card:
        fail("approved hard anchor cannot be overwritten: slot=%s card=%s" % (args.slot, old))
    if old == args.card and not args.note:
        fail("no change: slot=%s already %s" % (args.slot, args.card))
    look["slots"][args.slot]["card_id"] = args.card
    if args.note:
        look["slots"][args.slot]["note"] = args.note
    bump(look, args.actor, "patch", patch=[{"slot": args.slot, "from": old, "to": args.card}], note=args.note or "")
    snapshot(root, args.project, look)
    save_bible(root, args.project, bible)
    ok("patched %s slot=%s %s -> %s (v%d)" % (args.look, args.slot, old, args.card, look["version"]))


def cmd_propose(args):
    root = root_dir(args.root)
    bible = load_bible(root, args.project)
    look = get_look(bible, args.look)
    if look.get("status") != "Draft":
        fail("only Draft can be proposed (current: %s)" % look.get("status"))
    if not look.get("slots"):
        fail("cannot propose empty look")
    look["status"] = "Proposed"
    look["proposed_at"] = now()
    bump(look, args.actor, "propose", note=args.note or "submit for review")
    snapshot(root, args.project, look)
    save_bible(root, args.project, bible)
    ok("proposed %s v%d" % (args.look, look["version"]))


def _read_signature(path, reviewer):
    if not path:
        fail("approval requires --signature-file (human reviewer signature JSON)")
    p = Path(path)
    if not p.exists():
        fail("signature file not found: %s" % p)
    raw = p.read_bytes()
    try:
        sig = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        fail("signature file is not valid JSON: %s" % exc)
    if not isinstance(sig, dict):
        fail("signature file must be a JSON object")
    role = str(sig.get("role", "")).strip().lower()
    if role not in ("human", "reviewer"):
        fail("signature role must be human/reviewer (got %r); agent self-approval is forbidden" % role)
    if sig.get("agent_self_approval") is True:
        fail("agent self-approval is forbidden")
    signature = str(sig.get("signature", "")).strip()
    if not signature:
        fail("signature value is empty")
    sig_reviewer = str(sig.get("reviewer", "")).strip()
    if sig_reviewer and sig_reviewer != reviewer:
        fail("signature reviewer (%s) does not match --reviewer (%s)" % (sig_reviewer, reviewer))
    low = reviewer.strip().lower()
    if any(w == low or (" %s " % w) in (" %s " % low) for w in AGENT_WORDS):
        fail("agent/bot identity cannot approve; human reviewer required")
    return sig, hashlib.sha256(raw).hexdigest()


def cmd_approve(args):
    root = root_dir(args.root)
    bible = load_bible(root, args.project)
    look = get_look(bible, args.look)
    if look.get("status") != "Proposed":
        fail("only Proposed can be approved (current: %s)" % look.get("status"))
    if not args.reviewer:
        fail("approval requires --reviewer")
    sig, sig_hash = _read_signature(args.signature_file, args.reviewer)
    look["status"] = "Approved"
    look["approved_at"] = now()
    look["approved_by"] = args.reviewer
    hard = []
    soft = []
    for slot, item in sorted(look.get("slots", {}).items()):
        entry = {
            "slot": slot,
            "card_id": item["card_id"],
            "lock": item.get("lock", "soft"),
            "approved_by": args.reviewer,
            "approved_at": look["approved_at"],
        }
        (hard if entry["lock"] == "hard" else soft).append(entry)
    look["approved_anchors"] = {"hard": hard, "soft": soft}
    look.setdefault("approvals", []).append({
        "reviewer": args.reviewer,
        "role": str(sig.get("role")),
        "signature_file": str(Path(args.signature_file).resolve()),
        "signature_sha256": sig_hash,
        "approved_at": look["approved_at"],
        "note": args.note or "",
    })
    bump(look, args.actor, "approve", note=args.note or "reviewer=%s" % args.reviewer)
    snapshot(root, args.project, look)
    save_bible(root, args.project, bible)
    ok("approved %s v%d by %s" % (args.look, look["version"], args.reviewer))


def cmd_diff(args):
    root = root_dir(args.root)
    bible = load_bible(root, args.project)
    look = get_look(bible, args.look)
    cur = int(look["version"])
    v_from = int(args.from_version or max(1, cur - 1))
    v_to = int(args.to_version or cur)
    vdir = project_dir(root, args.project) / "versions" / args.look
    p_from, p_to = vdir / ("v%d.json" % v_from), vdir / ("v%d.json" % v_to)
    if not p_from.exists() or not p_to.exists():
        fail("version snapshot missing: %s / %s" % (p_from, p_to))
    a, b = loads(p_from), loads(p_to)
    sa, sb = a.get("slots", {}), b.get("slots", {})
    patches = []
    for slot in sorted(set(sa) | set(sb)):
        ca = (sa.get(slot) or {}).get("card_id")
        cb = (sb.get(slot) or {}).get("card_id")
        if ca != cb:
            patches.append({"slot": slot, "from": ca, "to": cb})
    out = {
        "look_id": args.look,
        "from_version": v_from,
        "to_version": v_to,
        "status": {"from": a.get("status"), "to": b.get("status")},
        "item_patch": patches,
        "item_patch_count": len(patches),
        "approved_anchors_changed": a.get("approved_anchors") != b.get("approved_anchors"),
        "note_changed": (a.get("rationale") != b.get("rationale")) or (a.get("scene_changes") != b.get("scene_changes")),
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        ok("diff %s v%d -> v%d | item patches: %d" % (args.look, v_from, v_to, len(patches)))
        for p in patches:
            ok("  %s: %s -> %s" % (p["slot"], p["from"], p["to"]))
    return out


def _card_ids_in_vault(vault):
    ids = set()
    for path in Path(vault).rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if not text.startswith("---"):
            continue
        for line in text.split("---", 2)[1].splitlines():
            if line.startswith("id:"):
                ids.add(line.split(":", 1)[1].strip().strip("'\""))
    return ids


def cmd_validate(args):
    root = root_dir(args.root)
    bible = load_bible(root, args.project)
    errors = []
    if not isinstance(bible.get("looks"), dict) or not bible["looks"]:
        errors.append("no looks")
    vault_ids = None
    if args.vault:
        vault_ids = _card_ids_in_vault(Path(args.vault))
    for lid, look in sorted(bible.get("looks", {}).items()):
        status = look.get("status")
        if status not in STATUSES:
            errors.append("%s: invalid status %r" % (lid, status))
        if not isinstance(look.get("version"), int) or look["version"] < 1:
            errors.append("%s: invalid version" % lid)
        if look.get("look_id") != lid:
            errors.append("%s: look_id mismatch" % lid)
        for slot, item in (look.get("slots") or {}).items():
            cid = item.get("card_id")
            if not CARD_ID_RE.match(str(cid)):
                errors.append("%s/%s: invalid card_id %r" % (lid, slot, cid))
            if vault_ids is not None and cid not in vault_ids:
                errors.append("%s/%s: card not in vault: %s" % (lid, slot, cid))
            if item.get("lock") not in ("hard", "soft"):
                errors.append("%s/%s: invalid lock %r" % (lid, slot, item.get("lock")))
        if status == "Approved":
            approvals = look.get("approvals") or []
            if not approvals:
                errors.append("%s: Approved without approval record" % lid)
            for ap in approvals:
                if not ap.get("reviewer") or not ap.get("signature_sha256"):
                    errors.append("%s: approval missing reviewer/signature" % lid)
            hard_slots = {a["slot"] for a in (look.get("approved_anchors") or {}).get("hard", [])}
            slot_hard = {s for s, i in (look.get("slots") or {}).items() if i.get("lock") == "hard"}
            if hard_slots != slot_hard:
                errors.append("%s: approved hard anchors do not match hard slots" % lid)
        if not (look.get("change_log") or []):
            errors.append("%s: empty change_log" % lid)
        vdir = project_dir(root, args.project) / "versions" / lid
        for v in [look.get("version")]:
            if not (vdir / ("v%d.json" % v)).exists():
                errors.append("%s: missing version snapshot v%s" % (lid, v))
    if errors:
        for e in errors:
            sys.stderr.write("ERROR: %s\n" % e)
        fail("look-bible validation failed (%d errors)" % len(errors))
    ok("validate PASS: %d look(s)" % len(bible["looks"]))
    return {"ok": True, "looks": len(bible["looks"]), "errors": []}


def cmd_migrate_aud004(args):
    """Create an AUD-004 slot-fix example under the template Look Bible."""
    root = root_dir(args.root)
    bdir = project_dir(root, args.project)
    example = {
        "audit_id": "AUD-004",
        "generated_at": now(),
        "description": "P3.5 Macbeth 18-look slot gaps fixed with existing cards; narrative unchanged.",
        "fixes": [
            {"look_id": "M2-B", "gap": "footwear", "patch": {"slot": "footwear", "card_id": "GAR-0081", "lock": "soft"},
             "source_cards": ["GAR-0081"], "note": "皮靴（15 世纪伦敦皮革踝靴，analogue）补足 footwear 槽；M2 叙事不变。"},
            {"look_id": "L3-A", "gap": "torso", "patch": {"slot": "torso", "card_id": "GAR-0079", "lock": "soft"},
             "source_cards": ["GAR-0079"], "note": "基尔特长袍（interpretive）作为 chemise 外的 torso 层；不改变梦游动作/叙事。"},
        ],
        "acceptance": ["18/18 looks have torso+footwear slots (or approved waiver)",
                       "M2-B footwear=GAR-0081", "L3-A torso=GAR-0079"],
    }
    dumps(bdir / "examples" / "aud-004-slotfix.json", example)
    ok("wrote %s" % (bdir / "examples" / "aud-004-slotfix.json"))


def build_parser():
    ap = argparse.ArgumentParser(prog="lookbook.py", description="Project-level Look Bible (Draft/Proposed/Approved)")
    ap.add_argument("--root", default=None, help="project root (default: repo root)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("--project", required=True); p.add_argument("--title", default=""); p.add_argument("--force", action="store_true"); p.set_defaults(func=cmd_init)
    p = sub.add_parser("list"); p.add_argument("--project", required=True); p.set_defaults(func=cmd_list)
    p = sub.add_parser("add"); p.add_argument("--project", required=True); p.add_argument("--look", required=True)
    p.add_argument("--character", default=""); p.add_argument("--slot", default=""); p.add_argument("--card", default="")
    p.add_argument("--lock", choices=["hard", "soft"], default=None); p.add_argument("--rationale", default="")
    p.add_argument("--note", default=""); p.add_argument("--source", action="append"); p.add_argument("--scene-change", action="append")
    p.add_argument("--actor", default="agent"); p.set_defaults(func=cmd_add)
    p = sub.add_parser("patch"); p.add_argument("--project", required=True); p.add_argument("--look", required=True)
    p.add_argument("--slot", required=True); p.add_argument("--card", required=True); p.add_argument("--note", default=""); p.add_argument("--actor", default="agent"); p.set_defaults(func=cmd_patch)
    p = sub.add_parser("propose"); p.add_argument("--project", required=True); p.add_argument("--look", required=True); p.add_argument("--note", default=""); p.add_argument("--actor", default="agent"); p.set_defaults(func=cmd_propose)
    p = sub.add_parser("approve"); p.add_argument("--project", required=True); p.add_argument("--look", required=True)
    p.add_argument("--reviewer", required=True); p.add_argument("--signature-file", required=True); p.add_argument("--note", default=""); p.add_argument("--actor", default="agent"); p.set_defaults(func=cmd_approve)
    p = sub.add_parser("diff"); p.add_argument("--project", required=True); p.add_argument("--look", required=True)
    p.add_argument("--from", dest="from_version", type=int); p.add_argument("--to", dest="to_version", type=int); p.add_argument("--json", action="store_true"); p.set_defaults(func=cmd_diff)
    p = sub.add_parser("validate"); p.add_argument("--project", required=True); p.add_argument("--vault", default=None); p.set_defaults(func=cmd_validate)
    p = sub.add_parser("migrate-aud004"); p.add_argument("--project", default="_template"); p.set_defaults(func=cmd_migrate_aud004)
    return ap


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
