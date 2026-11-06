import unittest

from gitquest.domain.answer_checker import (
    check_exact_answer,
    check_regex_answer,
    is_correct_answer,
    normalize_answer,
)
from gitquest.domain.missions import MISSIONS


REGEX_EXAMPLES = {
    4: (
        'git commit -m "Add player progress"',
        "git commit -m 'Add player progress'",
        'git commit -am "Fix mission copy"',
        "git commit -am 'Fix mission copy'",
    ),
    6: (
        "git switch -c feature/profile-page",
        "git checkout -b fix/login-form",
    ),
    8: (
        "git switch feature/profile-page",
        "git checkout fix/login-form",
    ),
    12: ("git branch feature/profile-page",),
    13: (
        "git switch main",
        "git checkout master",
    ),
    14: ("git branch -d feature/finished",),
    15: ("git branch -D experiment/abandoned",),
    16: ("git merge feature/profile-page",),
    17: ("git branch --all",),
}


INVALID_QUIZ_ANSWERS = {
    1: "git start",
    2: "git state",
    3: "git add README.md",
    4: "git commit",
    5: "git history",
    6: "git switch feature/existing",
    7: "git branch -a",
    8: "git switch -c feature/new",
    12: "git branch -d feature/profile",
    13: "git switch develop",
    14: "git branch feature/old-menu",
    15: "git branch feature/broken-test",
    16: "git rebase feature/login",
    17: "git branch",
}


class AnswerCheckerTests(unittest.TestCase):
    def test_normalize_answer_ignores_case_and_repeated_whitespace(self):
        self.assertEqual(normalize_answer("  Git   Status  "), "git status")

    def test_exact_checker_accepts_normalized_equivalent(self):
        self.assertTrue(check_exact_answer("  GIT   ADD   . ", ["git add ."]))

    def test_exact_checker_rejects_partial_or_unlisted_commands(self):
        self.assertFalse(check_exact_answer("git commit", ["git commit -m"]))
        self.assertFalse(check_exact_answer("git add README.md", ["git add ."]))

    def test_every_declared_exact_answer_is_accepted(self):
        for mission in MISSIONS:
            for answer in mission.get("accepted_answers", []):
                with self.subTest(mission_id=mission["id"], answer=answer):
                    self.assertTrue(is_correct_answer(answer, mission))

    def test_every_declared_regex_pattern_has_a_working_example(self):
        missions_with_patterns = {
            mission["id"]: mission for mission in MISSIONS if mission.get("accepted_patterns")
        }

        self.assertEqual(set(REGEX_EXAMPLES), set(missions_with_patterns))

        for mission_id, mission in missions_with_patterns.items():
            patterns = mission["accepted_patterns"]
            examples = REGEX_EXAMPLES[mission_id]
            self.assertEqual(
                len(examples),
                len(patterns),
                f"Mission {mission_id} needs one example per accepted pattern.",
            )

            for pattern, example in zip(patterns, examples):
                with self.subTest(mission_id=mission_id, pattern=pattern, example=example):
                    self.assertTrue(check_regex_answer(example, [pattern]))
                    self.assertTrue(is_correct_answer(example, mission))

    def test_regex_checker_is_case_insensitive_and_requires_a_full_match(self):
        pattern = r"git\s+switch\s+-c\s+[\w\-/]+"

        self.assertTrue(check_regex_answer("GIT SWITCH -C Feature/Profile", [pattern]))
        self.assertFalse(check_regex_answer("run git switch -c feature/profile", [pattern]))
        self.assertFalse(check_regex_answer("git switch -c feature/profile now", [pattern]))

    def test_each_quiz_mission_rejects_a_related_incorrect_command(self):
        quiz_missions = {
            mission["id"]: mission
            for mission in MISSIONS
            if mission.get("mission_type", "quiz") == "quiz"
        }

        self.assertEqual(set(INVALID_QUIZ_ANSWERS), set(quiz_missions))

        for mission_id, mission in quiz_missions.items():
            answer = INVALID_QUIZ_ANSWERS[mission_id]
            with self.subTest(mission_id=mission_id, answer=answer):
                self.assertFalse(is_correct_answer(answer, mission))

    def test_sandbox_missions_do_not_accept_text_answers(self):
        sandbox_missions = [
            mission for mission in MISSIONS if mission.get("mission_type") == "sandbox"
        ]

        self.assertGreater(len(sandbox_missions), 0)
        for mission in sandbox_missions:
            with self.subTest(mission_id=mission["id"]):
                self.assertFalse(is_correct_answer("git init", mission))


if __name__ == "__main__":
    unittest.main()
