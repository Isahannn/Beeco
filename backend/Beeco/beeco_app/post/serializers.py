from rest_framework import serializers
from .models import Post, Comment, Like, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), write_only=True, many=True, required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'user', 'tags', 'tag_ids']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'tags']

    def create(self, validated_data):
        tags = validated_data.pop('tag_ids', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_ids', None)
        instance = super().update(instance, validated_data)
        if tags is not None:
            instance.tags.set(tags)
        return instance


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'parent_comment', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get("parent_comment") and data["parent_comment"].post != data["post"]:
            raise serializers.ValidationError("Parent comment must belong to the same post.")
        return data


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        post = data.get('post')
        if Like.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("You already liked this post.")
        return data
